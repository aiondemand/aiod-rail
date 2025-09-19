import { Routes } from '@angular/router';
import { DOCS_NAV } from './features/docs/pages/docs.nav';
import { DATASETS_NAV } from './features/datasets/pages/datasets.nav';
import { EXPERIMENTS_NAV } from './features/experiments/pages/experiments.nav';

export const routes: Routes = [
  // default redirect
  { path: '', pathMatch: 'full', redirectTo: 'docs/about' },

  // EXPERIMENTS
  {
    path: 'experiments',
    data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'public' },
      {
        path: 'public',
        loadComponent: () =>
          import('./features/experiments/pages/public/public').then((m) => m.PublicPage),
      },
      {
        path: 'my-experiments',
        loadComponent: () =>
          import('./features/experiments/pages/my-experiments/my-experiments').then(
            (m) => m.MyExperiments
          ),
      },
      {
        path: 'create-experiment',
        loadComponent: () =>
          import('./features/experiments/pages/create-experiment/create-experiment').then(
            (m) => m.CreateExperiment
          ),
      },
      {
        path: 'templates',
        loadComponent: () =>
          import('./features/experiments/pages/templates/templates').then((m) => m.TemplatesPage),
      },
      {
        path: 'my-templates',
        loadComponent: () =>
          import('./features/experiments/pages/my-templates/my-templates').then(
            (m) => m.MyTemplates
          ),
      },
      {
        path: 'my-templates',
        loadComponent: () =>
          import('./features/experiments/pages/my-templates/my-templates').then(
            (m) => m.MyTemplates
          ),
      },
      {
        path: 'create-template',
        loadComponent: () =>
          import('./features/experiments/pages/create-template/create-template').then(
            (m) => m.CreateTemplate
          ),
      },
    ],
  },

  // DATASETS
  {
    path: 'datasets',
    data: { sidenav: DATASETS_NAV, baseLink: '/datasets' },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'all' },
      {
        path: 'all',
        loadComponent: () =>
          import('./features/datasets/pages/all/all').then((m) => m.AllDatasetsPage),
      },
      {
        path: 'create-dataset',
        loadComponent: () =>
          import('./features/datasets/pages/create-dataset/create-dataset').then(
            (m) => m.CreateDataset
          ),
      },
      {
        path: 'my-datasets',
        loadComponent: () =>
          import('./features/datasets/pages/my-datasets/my-datasets').then((m) => m.MyDatasets),
      },
    ],
  },

  // DOCS
  {
    path: 'docs',
    data: { sidenav: DOCS_NAV, baseLink: '/docs' },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'about' },
      {
        path: 'about',
        loadComponent: () =>
          import('./features/docs/pages/about-page/about-page').then((m) => m.AboutPage),
      },
      {
        path: 'main-concepts',
        loadComponent: () =>
          import('./features/docs/pages/main-concepts-page/main-concepts-page').then(
            (m) => m.MainConceptsPage
          ),
      },
      {
        path: 'main-concepts-template',
        loadComponent: () =>
          import(
            './features/docs/pages/main-concepts-template-page/main-concepts-template-page'
          ).then((m) => m.MainConceptsTemplatePage),
      },
      {
        path: 'main-concepts-experiments',
        loadComponent: () =>
          import(
            './features/docs/pages/main-concepts-experiments-page/main-concepts-experiments-page'
          ).then((m) => m.MainConceptsExperimentsPage),
      },
      {
        path: 'main-concepts-run',
        loadComponent: () =>
          import('./features/docs/pages/main-concepts-run-page/main-concepts-run-page').then(
            (m) => m.MainConceptsRunPage
          ),
      },
      {
        path: 'main-concepts-run',
        loadComponent: () =>
          import('./features/docs/pages/main-concepts-run-page/main-concepts-run-page').then(
            (m) => m.MainConceptsRunPage
          ),
      },
      {
        path: 'rail-sdks',
        loadComponent: () =>
          import('./features/docs/pages/rail-sdks/rail-sdks').then((m) => m.RailSDKs),
      },
      {
        path: 'outer-sdk',
        loadComponent: () =>
          import('./features/docs/pages/outer-sdk/outer-sdk').then((m) => m.OuterSDK),
      },
      {
        path: 'inner-sdk',
        loadComponent: () =>
          import('./features/docs/pages/inner-sdk/inner-sdk').then((m) => m.InnerSDK),
      },
    ],
  },

  // fallback
  { path: '**', redirectTo: 'docs/about' },
];
