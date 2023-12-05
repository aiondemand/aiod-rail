import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { OAuthService } from 'angular-oauth2-oidc';

export const authGuard: CanActivateFn = (route, state) => {
  const oauthService = inject(OAuthService);

  if (!oauthService.hasValidAccessToken()) {
    oauthService.initLoginFlow();
    return false;
  }

  return true;
};
