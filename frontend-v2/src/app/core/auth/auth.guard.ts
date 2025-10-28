import { inject, PLATFORM_ID } from '@angular/core';
import { CanActivateFn, CanMatchFn, Router, UrlTree } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
import { AuthService } from './auth.service';

function ensureLoginOrBlock(): boolean | UrlTree {
  const platformId = inject(PLATFORM_ID);
  const auth = inject(AuthService);
  const router = inject(Router);

  const logged = auth.isLoggedIn();
  if (logged) return true;

  if (isPlatformBrowser(platformId)) {
    auth.login();
    return false;
  }

  return router.createUrlTree(['/docs/about']);
}

/** CanActivate  */
export const authGuard: CanActivateFn = () => ensureLoginOrBlock();
/** CanMatch  ( lazy ) */
export const authMatchGuard: CanMatchFn = () => ensureLoginOrBlock();

function ensureAdmin(): boolean | UrlTree {
  const auth = inject(AuthService);
  const router = inject(Router);
  const ok = auth.isLoggedIn() && auth.hasAdminRole();
  return ok ? true : router.createUrlTree(['/docs/about']);
}

export const adminGuard: CanActivateFn = () => ensureAdmin();
export const adminMatchGuard: CanMatchFn = () => ensureAdmin();
