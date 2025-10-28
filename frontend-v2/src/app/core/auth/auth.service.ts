// src/app/core/auth/auth.service.ts
import { Injectable, PLATFORM_ID, computed, inject, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { OAuthEvent, OAuthService, UserInfo } from 'angular-oauth2-oidc';
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
  private _claimsReady = signal(false);

  // ===== PUBLIC COMPUTEDS =====

  isLoggedIn = computed(() => this._loggedIn());

  /** Login for ui */
  isLoggedInUI = computed(() => this._loggedIn() && this._claimsReady());

  userName = computed(() => {
    const c = this._claims();
    if (!c) return '';
    const gn = c['given_name'] ?? '';
    const fn = c['family_name'] ?? '';
    const name = c['name'] ?? '';
    const pref = c['preferred_username'] ?? '';
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

  // ===== INIT (called from APP_INITIALIZER) =====
  async init(): Promise<void> {
    if (!isPlatformBrowser(this.platformId)) return;

    this.oauth.configure(buildAuthConfig());
    this.oauth.setStorage(localStorage);

    // Relevant events
    this.oauth.events
      .pipe(
        filter((e: OAuthEvent) =>
          [
            'token_received',
            'token_refreshed',
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
          case 'token_refresh_error':
          case 'session_terminated':
          case 'logout': {
            this.hardSignOut();
            return;
          }
          case 'token_expires': {
            if (!this.oauth.hasValidAccessToken()) this.softSignOut();
            return;
          }
          case 'token_received':
          case 'token_refreshed': {
            this.updateLoggedInFlag();

            this._claimsReady.set(false);

            void this.ensureClaimsLoaded();
            return;
          }
        }
      });

    // 1) Discovery + try login
    await this.oauth.loadDiscoveryDocument();
    const tryCodeFlow = (this.oauth as any).tryLoginCodeFlow?.bind(this.oauth);
    if (tryCodeFlow) await tryCodeFlow();
    else await this.oauth.loadDiscoveryDocumentAndTryLogin();

    this.updateLoggedInFlag();

    if (this._loggedIn()) {
      this._claimsReady.set(false);
      await this.ensureClaimsLoaded();
    } else {
      this.clearLocalOnly();
    }

    // Silent refresh
    this.oauth.setupAutomaticSilentRefresh();

    // Heartbeat – every 60s revalide access token
    setInterval(() => this.updateLoggedInFlag(), 60000);
  }

  // ===== HELPERS =====

  private updateLoggedInFlag() {
    const valid = this.oauth.hasValidAccessToken();
    this._loggedIn.set(valid);
    if (!valid) {
      this._claims.set(null);
      this._claimsReady.set(false);
    }
  }

  private async ensureClaimsLoaded() {
    try {
      const idClaims = (this.oauth.getIdentityClaims() as Record<string, any> | null) ?? {};

      const profile = (await this.oauth.loadUserProfile()) as UserInfo & Record<string, any>;

      this._claims.set({ ...(idClaims ?? {}), ...(profile ?? {}) });
    } catch {
      const idClaims = (this.oauth.getIdentityClaims() as Record<string, any> | null) ?? null;
      this._claims.set(idClaims);
    } finally {
      this._claimsReady.set(true);
    }
  }

  private clearLocalOnly() {
    try {
      (this.oauth as any).clearStorage?.();
    } catch {}
    this._claims.set(null);
    this._claimsReady.set(false);
  }

  private softSignOut() {
    this._claims.set(null);
    this._claimsReady.set(false);
    this._loggedIn.set(false);
  }

  private hardSignOut() {
    this.clearLocalOnly();
    this._loggedIn.set(false);
  }

  // ===== PUBLIC HELPERS =====
  async waitUntilClaimsReady(): Promise<void> {
    if (this._claimsReady()) return;
    await new Promise<void>((resolve) => {
      const t = setInterval(() => {
        if (this._claimsReady()) {
          clearInterval(t);
          resolve();
        }
      }, 50);
    });
  }

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

  // ===== API =====
  login(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    this.oauth.initLoginFlow();
  }

  logout(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    this.oauth.logOut();
    this._claims.set(null);
    this._claimsReady.set(false);
    this._loggedIn.set(false);
  }
}
