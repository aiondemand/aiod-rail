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

  // ===== PUBLIC COMPUTEDS =====
  isLoggedIn = computed(() => this._loggedIn());
  userName = computed(() => {
    const c = this._claims();
    if (!c) return '';
    const gn = c['given_name'] ?? '';
    const fn = c['family_name'] ?? '';
    const pref = c['preferred_username'] ?? '';
    return gn || fn ? `${gn} ${fn}`.trim() : pref;
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
    return true;
    return this.clientRoles().includes('admin_access') || this.userRoles().includes('admin');
  });

  // ===== INIT (called from APP_INITIALIZER) =====
  async init(): Promise<void> {
    if (!isPlatformBrowser(this.platformId)) return;

    this.oauth.configure(buildAuthConfig());
    this.oauth.setStorage(localStorage);

    // Reaguj na token/profile udalosti (bez spamovania)
    this.oauth.events
      .pipe(
        filter((e: OAuthEvent) =>
          [
            'token_received',
            'token_refreshed',
            'user_profile_loaded',
            'session_terminated',
            'session_error',
          ].includes(e.type)
        )
      )
      .subscribe((e) => {
        if (
          e.type === 'token_received' ||
          e.type === 'token_refreshed' ||
          e.type === 'session_terminated'
        ) {
          this.updateLoggedInFlag('event');
        }
      });

    // 1) Discovery & login code flow
    await this.oauth.loadDiscoveryDocument();
    const tryCodeFlow = (this.oauth as any).tryLoginCodeFlow?.bind(this.oauth);
    if (tryCodeFlow) await tryCodeFlow();
    else await this.oauth.loadDiscoveryDocumentAndTryLogin();

    // 2) Flag + auto refresh + claims
    this.updateLoggedInFlag('post-try-login');
    this.oauth.setupAutomaticSilentRefresh();
    if (this._loggedIn()) await this.refreshClaims();

    // 3) Microtask – stabilizácia + expose debug API
  }

  // ===== HELPERS =====
  private updateLoggedInFlag(source: string) {
    const flag = !!this.oauth.getAccessToken() || !!this.oauth.getIdToken();
    this._loggedIn.set(flag);
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

  // ===== PUBLIC DEBUG HELPERS =====

  getAccessToken(): string | null {
    try {
      return this.oauth.getAccessToken() || null;
    } catch {
      return null;
    }
  }

  /**  Authorization header  */
  getAuthHeaders(): Record<string, string> | undefined {
    const t = this.getAccessToken();
    return t ? { Authorization: `Bearer ${t}` } : undefined;
  }

  dump(): void {
    const access = this.getAccessToken();
    const id = this.oauth.getIdToken();
    const expMs = this.oauth.getAccessTokenExpiration() || 0;
    const secs = expMs ? Math.max(0, Math.floor((expMs - Date.now()) / 1000)) : 0;
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
    this._loggedIn.set(false);
  }
}
