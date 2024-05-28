import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { authConfig } from 'src/keycloak.config';
import { filter } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  isLoggedIn = false;

  constructor(private oauthService: OAuthService) {
    this.oauthService.configure(authConfig);
    this.oauthService.loadDiscoveryDocumentAndTryLogin();
    this.oauthService.setupAutomaticSilentRefresh();

    this.oauthService.events
      .pipe(
        filter((e) => e.type === 'token_received')
      )
      .subscribe((_) => {
        this.oauthService.loadUserProfile();
        this.isLoggedIn = this.oauthService.hasValidIdToken();
      });
  }

  ngOnInit() {
    this.isLoggedIn = this.oauthService.hasValidIdToken();
  }

  login(): void {
    this.oauthService.initLoginFlow();
  }

  logout(): void {
    this.oauthService.logOut();
  }

  get hasAdminRole(): boolean {
    return this.clientRoles.includes('admin_access')
  }

  get userName(): string {
    const claims = this.oauthService.getIdentityClaims() as any;
    return claims ? claims['given_name'] + " " + claims['family_name'] : "";
  }

  get userRoles(): string[] {
    const claims = this.oauthService.getIdentityClaims() as any;
    return claims ? claims.roles : [];
  }

  get clientRoles(): string[] {
    const claims = this.oauthService.getIdentityClaims() as any;
    if (claims && claims.resource_access && claims.resource_access[environment.AIOD_KEYCLOAK_CLIENT_ID_BACKEND]) {
      return claims.resource_access[environment.AIOD_KEYCLOAK_CLIENT_ID_BACKEND]?.roles || [];
    }
    return [];
  }
}
