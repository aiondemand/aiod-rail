import { AuthConfig } from 'angular-oauth2-oidc';
import { environment } from '../../../environments/environment';

export const buildAuthConfig = (): AuthConfig => {
  const isBrowser = typeof window !== 'undefined' && !!window.location;
  const origin = isBrowser ? window.location.origin : '';
  const pathname = isBrowser ? window.location.pathname : '/';

  const cfg: AuthConfig = {
    issuer: `${environment.AIOD_KEYCLOAK_URL}/realms/${environment.AIOD_KEYCLOAK_REALM}`,
    clientId: environment.AIOD_KEYCLOAK_CLIENT_ID,
    redirectUri: origin + pathname,
    responseType: 'code',
    scope: 'openid profile email',
    useSilentRefresh: false,
    showDebugInformation: true,
    requireHttps: false,
  };

  return cfg;
};
