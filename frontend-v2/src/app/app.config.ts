import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZonelessChangeDetection,
  importProvidersFrom,
  APP_INITIALIZER,
  PLATFORM_ID,
} from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { provideRouter } from '@angular/router';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideHttpClient, withFetch, withInterceptorsFromDi } from '@angular/common/http';

import { MarkdownModule, MARKED_OPTIONS } from 'ngx-markdown';

import { routes } from './app.routes';
import { provideHighlightOptions } from 'ngx-highlightjs';

import { provideOAuthClient, OAuthStorage } from 'angular-oauth2-oidc';
import { environment } from '../environments/environment';
import { AuthService } from './core/auth/auth.service';

function hljsLoader() {
  return async () => {
    if (typeof window === 'undefined') return;
    const mod = await import('highlight.js');
    (window as any).hljs = (mod as any).default ?? mod;
  };
}

class MemoryStorage implements OAuthStorage {
  private data = new Map<string, string>();
  getItem(k: string) {
    return this.data.get(k) ?? null;
  }
  setItem(k: string, v: string) {
    this.data.set(k, v);
  }
  removeItem(k: string) {
    this.data.delete(k);
  }
  clear() {
    this.data.clear();
  }
}
function oauthStorageFactory(platformId: object): OAuthStorage {
  return isPlatformBrowser(platformId) ? localStorage : new MemoryStorage();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideHttpClient(withFetch(), withInterceptorsFromDi()),

    provideHighlightOptions({
      fullLibraryLoader: () => import('highlight.js'),
    }),

    importProvidersFrom(
      MarkdownModule.forRoot({
        markedOptions: {
          provide: MARKED_OPTIONS,
          useValue: {
            gfm: true,
            breaks: true,
          } as any,
        },
      })
    ),

    provideOAuthClient({
      resourceServer: { allowedUrls: [environment.BACKEND_API_URL], sendAccessToken: true },
    }),
    { provide: OAuthStorage, useFactory: oauthStorageFactory, deps: [PLATFORM_ID] },

    // Auth bootstrap
    {
      provide: APP_INITIALIZER,
      multi: true,
      useFactory: (auth: AuthService) => () => auth.init(),
      deps: [AuthService],
    },

    { provide: APP_INITIALIZER, multi: true, useFactory: hljsLoader },
  ],
};
