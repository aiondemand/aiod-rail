import { Routes } from '@angular/router';
import { authMatchGuard, authGuard } from './core/auth/auth.guard';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'docs/about' },

  { path: 'templates/:id', pathMatch: 'full', redirectTo: 'experiments/templates/:id' },

  // ===== EXPERIMENTS =====
  {
    path: 'experiments',
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'public' },

      {
        path: 'public',
        loadComponent: () =>
          import('./features/experiments/pages/public/public').then((m) => m.PublicPage),
      },

      // chránené moje zoznamy + create
      {
        path: 'my-experiments',
        canMatch: [authMatchGuard],
        loadComponent: () =>
          import('./features/experiments/pages/my-experiments/my-experiments').then(
            (m) => m.MyExperiments
          ),
      },
      {
        path: 'create-experiment',
        canMatch: [authMatchGuard],
        loadComponent: () =>
          import('./features/experiments/pages/create-experiment/create-experiment').then(
            (m) => m.CreateExperiment
          ),
      },

      // templates (list + detail)
      {
        path: 'templates',
        children: [
          {
            path: '',
            loadComponent: () =>
              import('./features/experiments/pages/templates/templates').then(
                (m) => m.TemplatesPage
              ),
          },
          {
            path: ':id',
            loadComponent: () =>
              import('./features/experiments/pages/template-detail/template-detail').then(
                (m) => m.TemplateDetailPage
              ),
          },
        ],
      },

      // chránené „moje“ / create templates
      {
        path: 'my-templates',
        canMatch: [authMatchGuard],
        loadComponent: () =>
          import('./features/experiments/pages/my-templates/my-templates').then(
            (m) => m.MyTemplates
          ),
      },
      {
        path: 'create-template',
        canMatch: [authMatchGuard],
        loadComponent: () =>
          import('./features/experiments/pages/create-template/create-template').then(
            (m) => m.CreateTemplate
          ),
      },

      {
        path: 'runs/:runId',
        loadComponent: () =>
          import('./features/experiments/pages/experiment-run-detial/experiment-run-detail').then(
            (m) => m.ExperimentRunDetailComponent
          ),
      },
      {
        path: ':id',
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
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'all' },

      {
        path: 'all',
        loadComponent: () =>
          import('./features/datasets/pages/all/all').then((m) => m.DatasetsAllComponent),
      },
      {
        path: 'my-datasets',
        canMatch: [authMatchGuard],
        loadComponent: () =>
          import('./features/datasets/pages/my-datasets/my-datasets').then((m) => m.MyDatasets),
      },
      {
        path: 'create-dataset',
        canMatch: [authMatchGuard],
        loadComponent: () =>
          import('./features/datasets/pages/create-dataset/create-dataset').then(
            (m) => m.CreateDataset
          ),
      },
      {
        path: ':id',
        loadComponent: () =>
          import('./features/datasets/pages/dataset-detail/dataset-detail').then(
            (m) => m.DatasetDetailComponent
          ),
      },
    ],
  },

  // ===== PROFILE =====
  {
    path: 'profile',
    canActivate: [authGuard],
    loadComponent: () => import('./features/profile/profile').then((m) => m.ProfilePage),
  },

  // ===== DOCS =====
  {
    path: 'docs',
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

  { path: '**', redirectTo: 'docs/about' },
];
