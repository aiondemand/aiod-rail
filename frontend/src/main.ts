import { bootstrapApplication } from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import { App } from './app/app';
import { appConfig } from './app/app.config';

import { CodeEditorModule } from '@ngstack/code-editor';

bootstrapApplication(App, {
  providers: [
    ...(appConfig.providers || []),
    importProvidersFrom(CodeEditorModule.forRoot({ baseUrl: 'assets/monaco' })),
  ],
}).catch((err) => console.error(err));
