import { Injectable, PLATFORM_ID, computed, inject, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { OAuthService, UserInfo, OAuthEvent } from 'angular-oauth2-oidc';
import { filter } from 'rxjs';
import { buildAuthConfig } from './auth.config';
import { environment } from '../../../environments/environment';

type Claims = Record<string, any> | null;
type ClaimsWithRoles = {
  roles?: string[];
  resource_access?: Record<string, { roles?: string[] }>;
} & Record<string, any>;

@Injectable({ providedIn: 'root' })
export class AuthService {
  private platformId = inject(PLATFORM_ID);
  private oauth = inject(OAuthService);

  // ===== STATE =====
  private _claims = signal<Claims>(null);
  private _loggedIn = signal(false);
  private expiryTimer: any = null;

  // ===== COMPUTED SIGNALS =====
  isLoggedIn = computed(() => this._loggedIn());

  userName = computed(() => {
    const c = this._claims();
    if (!c) return '';
    const gn = c['given_name'] ?? '';
    const fn = c['family_name'] ?? '';
    const pref = c['preferred_username'] ?? '';
    const name = c['name'] ?? '';
    const email = c['email'] ?? '';
    return gn || fn ? `${gn} ${fn}`.trim() : name || pref || email || '';
  });

  userRoles = computed<string[]>(() => {
    const c = this._claims() as ClaimsWithRoles | null;
    return Array.isArray(c?.roles) ? c.roles! : [];
  });

  clientRoles = computed<string[]>(() => {
    const c = this._claims() as ClaimsWithRoles | null;
    const client = environment.AIOD_KEYCLOAK_CLIENT_ID_BACKEND;
    const roles = c?.resource_access?.[client]?.roles;
    return Array.isArray(roles) ? roles : [];
  });

  hasAdminRole = computed<boolean>(() => {
    return this.clientRoles().includes('admin_access') || this.userRoles().includes('admin');
  });

  // ===== INITIALIZATION (called from APP_INITIALIZER) =====
  async init(): Promise<void> {
    if (!isPlatformBrowser(this.platformId)) return;

    this.oauth.configure(buildAuthConfig());
    this.oauth.setStorage(localStorage);

    this.oauth.events
      .pipe(
        filter((e: OAuthEvent) =>
          [
            'token_received',
            'token_refreshed',
            'user_profile_loaded',
            'token_expires',
            'token_refresh_error',
            'session_terminated',
            'session_error',
            'logout',
          ].includes(e.type)
        )
      )
      .subscribe((e) => {
        switch (e.type) {
          case 'token_received':
          case 'token_refreshed': {
            this.updateLoggedInFlag();
            this.scheduleExpiryWatcher();
            void this.refreshClaims();
            return;
          }
          case 'token_expires': {
            if (!this.oauth.hasValidAccessToken()) {
              this._claims.set(null);
              this._loggedIn.set(false);
            }
            return;
          }
          case 'token_refresh_error':
          case 'session_terminated':
          case 'logout': {
            this.clearLoginState();
            return;
          }
        }
      });

    // Cross-tab sync (logout/login in another tab)
    window.addEventListener('storage', (e: StorageEvent) => {
      if (e.storageArea !== localStorage) return;
      const key = e.key ?? '';
      if (/(access_token|id_token|expires_at|refresh_token|oauth|oidc)/i.test(key)) {
        this.updateLoggedInFlag();
        this.scheduleExpiryWatcher();
        if (this._loggedIn()) void this.refreshClaims();
        else this._claims.set(null);
      }
    });

    // Visibility event (tab focus)
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) return;
      this.updateLoggedInFlag();
      this.scheduleExpiryWatcher();
      if (this._loggedIn()) void this.refreshClaims();
    });

    // Discovery + login
    await this.oauth.loadDiscoveryDocument();
    const tryCodeFlow = (this.oauth as any).tryLoginCodeFlow?.bind(this.oauth);
    if (tryCodeFlow) await tryCodeFlow();
    else await this.oauth.loadDiscoveryDocumentAndTryLogin();

    // Initial token + claims
    this.updateLoggedInFlag();
    this.scheduleExpiryWatcher();

    if (this._loggedIn()) await this.refreshClaims();
    else {
      this.clearLocalArtifacts();
      this._claims.set(null);
    }

    // Enable silent token refresh
    this.oauth.setupAutomaticSilentRefresh();
  }

  // ===== HELPERS =====

  private updateLoggedInFlag() {
    const flag = this.oauth.hasValidAccessToken();
    this._loggedIn.set(flag);
    if (!flag) this._claims.set(null);
  }

  private scheduleExpiryWatcher() {
    if (this.expiryTimer) {
      clearTimeout(this.expiryTimer);
      this.expiryTimer = null;
    }
    const expMs = this.oauth.getAccessTokenExpiration() || 0;
    if (!expMs) return;
    const delay = Math.max(0, expMs - Date.now() + 100);
    this.expiryTimer = setTimeout(() => {
      this.updateLoggedInFlag();
    }, delay);
  }

  private async refreshClaims() {
    try {
      const profile = (await this.oauth.loadUserProfile()) as UserInfo & Record<string, any>;
      const idClaims = this.oauth.getIdentityClaims() as Record<string, any> | null;
      this._claims.set({ ...(idClaims ?? {}), ...(profile ?? {}) });
    } catch {
      const idClaims = this.oauth.getIdentityClaims() as Record<string, any> | null;
      this._claims.set(idClaims ?? null);
    }
  }

  private clearLocalArtifacts() {
    try {
      (this.oauth as any).clearStorage?.();
    } catch {}
  }

  private clearLoginState() {
    this._claims.set(null);
    this._loggedIn.set(false);
    this.clearLocalArtifacts();
    if (this.expiryTimer) {
      clearTimeout(this.expiryTimer);
      this.expiryTimer = null;
    }
  }

  // ===== PUBLIC API =====

  getAccessToken(): string | null {
    try {
      return this.oauth.getAccessToken() || null;
    } catch {
      return null;
    }
  }

  getAuthHeaders(): Record<string, string> | undefined {
    const t = this.getAccessToken();
    return t ? { Authorization: `Bearer ${t}` } : undefined;
  }

  login(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    this.oauth.initLoginFlow();
  }

  logout(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    this.oauth.logOut();
    this.clearLoginState();
  }
}
