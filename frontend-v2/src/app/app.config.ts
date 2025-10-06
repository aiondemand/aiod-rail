import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZonelessChangeDetection,
  importProvidersFrom,
  APP_INITIALIZER,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideHttpClient, withFetch } from '@angular/common/http';

import { MarkdownModule, MARKED_OPTIONS } from 'ngx-markdown';
import { MarkedOptions } from 'marked';
import { routes } from './app.routes';
import { provideHighlightOptions } from 'ngx-highlightjs';

async function prismLoader() {
  if (typeof window === 'undefined') return;
  const prismMod = await import('prismjs');
  const Prism = (prismMod as any).default ?? prismMod;
  await Promise.all([
    import('prismjs/components/prism-python'),
    import('prismjs/components/prism-properties'),
    import('prismjs/components/prism-json'),
  ]);
  (window as any).Prism = Prism;
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideHttpClient(withFetch()),
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
            headerIds: true,
            mangle: false,
          } as MarkedOptions,
        },
      })
    ),

    {
      provide: APP_INITIALIZER,
      multi: true,
      useFactory: () => prismLoader,
    },
  ],
};
