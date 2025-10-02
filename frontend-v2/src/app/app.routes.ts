import { Routes } from '@angular/router';
import { DOCS_NAV } from './features/docs/pages/docs.nav';
import { DATASETS_NAV } from './features/datasets/pages/datasets.nav';
import { EXPERIMENTS_NAV } from './features/experiments/pages/experiments.nav';

export const routes: Routes = [
  // default
  { path: '', pathMatch: 'full', redirectTo: 'docs/about' },

  // ===== EXPERIMENTS =====
  {
    path: 'experiments',
    data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'public' },

      // runs detail: /experiments/runs/:runId
      {
        path: 'runs/:runId',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        loadComponent: () =>
          import('./features/experiments/pages/experiment-run-detial/experiment-run-detail').then(
            (m) => m.ExperimentRunDetailComponent
          ),
      },

      // list of public experiments
      {
        path: 'public',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        loadComponent: () =>
          import('./features/experiments/pages/public/public').then((m) => m.PublicPage),
      },

      // my experiments
      {
        path: 'my-experiments',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        loadComponent: () =>
          import('./features/experiments/pages/my-experiments/my-experiments').then(
            (m) => m.MyExperiments
          ),
      },

      // create experiment
      {
        path: 'create-experiment',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        loadComponent: () =>
          import('./features/experiments/pages/create-experiment/create-experiment').then(
            (m) => m.CreateExperiment
          ),
      },

      // ===== TEMPLATES  =====
      {
        path: 'templates',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        children: [
          {
            path: '',
            loadComponent: () =>
              import('./features/experiments/pages/templates/templates').then(
                (m) => m.TemplatesPage
              ),
          },

          // {
          //   path: ':id',
          //   loadComponent: () => import('./features/experiments/pages/template-detail/template-detail')
          //     .then(m => m.TemplateDetailPage),
          // },
        ],
      },

      // my templates (list)
      {
        path: 'my-templates',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        loadComponent: () =>
          import('./features/experiments/pages/my-templates/my-templates').then(
            (m) => m.MyTemplates
          ),
      },

      // create template
      {
        path: 'create-template',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        loadComponent: () =>
          import('./features/experiments/pages/create-template/create-template').then(
            (m) => m.CreateTemplate
          ),
      },

      // ===== EXPERIMENT detail =====
      {
        path: ':id',
        data: { sidenav: EXPERIMENTS_NAV, baseLink: '/experiments' },
        loadComponent: () =>
          import('./features/experiments/pages/experiment-detail/experiment-detail').then(
            (m) => m.ExperimentDetailPage
          ),
      },
    ],
  },

  // ===== DATASETS =====
  {
    path: 'datasets',
    data: { sidenav: DATASETS_NAV, baseLink: '/datasets' },
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'all' },

      // listing
      {
        path: 'all',
        data: { sidenav: DATASETS_NAV, baseLink: '/datasets' },
        loadComponent: () =>
          import('./features/datasets/pages/all/all').then((m) => m.DatasetsAllComponent),
      },

      // my datasets
      {
        path: 'my-datasets',
        data: { sidenav: DATASETS_NAV, baseLink: '/datasets' },
        loadComponent: () =>
          import('./features/datasets/pages/my-datasets/my-datasets').then((m) => m.MyDatasets),
      },

      // create dataset
      {
        path: 'create-dataset',
        data: { sidenav: DATASETS_NAV, baseLink: '/datasets' },
        loadComponent: () =>
          import('./features/datasets/pages/create-dataset/create-dataset').then(
            (m) => m.CreateDataset
          ),
      },

      // --- DETAIL /datasets/:id ---
      {
        path: ':id',
        data: { sidenav: DATASETS_NAV, baseLink: '/datasets' },
        loadComponent: () =>
          import('./features/datasets/pages/dataset-detail/dataset-detail').then(
            (m) => m.DatasetDetailComponent
          ),
      },

      // ---  /datasets/all/:id -> /datasets/:id ---
      { path: 'all/:id', pathMatch: 'full', redirectTo: '/datasets/:id' },
    ],
  },

  // ===== DOCS =====
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
