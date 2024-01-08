import { environment } from './environments/environment';

import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  issuer: `${environment.AIOD_KEYCLOAK_URL}/realms/${environment.AIOD_KEYCLOAK_REALM}`,
  clientId: environment.AIOD_KEYCLOAK_CLIENT_ID,
  redirectUri: window.location.origin + '/',
  responseType: 'code',
  scope: 'openid profile email',
  showDebugInformation: true,
  requireHttps: false
};
