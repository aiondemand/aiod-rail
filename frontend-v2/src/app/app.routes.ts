import { Routes } from '@angular/router';
import { adminGuard, authGuard } from './core/auth/auth.guard';

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

      {
        path: 'my-experiments',
        canMatch: [authGuard],
        loadComponent: () =>
          import('./features/experiments/pages/my-experiments/my-experiments').then(
            (m) => m.MyExperimentsPage
          ),
      },
      {
        path: 'create-experiment',
        canMatch: [authGuard],
        loadComponent: () =>
          import('./features/experiments/pages/create-experiment/create-experiment').then(
            (m) => m.CreateExperimentPage
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
          {
            path: ':id/update',
            canMatch: [authGuard],
            loadComponent: () =>
              import('./features/experiments/pages/create-template/create-template').then(
                (m) => m.CreateTemplatePage
              ),
          },
        ],
      },

      // create templates
      {
        path: 'my-templates',
        canMatch: [authGuard],
        loadComponent: () =>
          import('./features/experiments/pages/my-templates/my-templates').then(
            (m) => m.MyTemplatesPage
          ),
      },
      {
        path: 'create-template',
        canMatch: [authGuard],
        loadComponent: () =>
          import('./features/experiments/pages/create-template/create-template').then(
            (m) => m.CreateTemplatePage
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
      {
        path: ':id/update',
        canMatch: [authGuard],
        loadComponent: () =>
          import('./features/experiments/pages/create-experiment/create-experiment').then(
            (m) => m.CreateExperimentPage
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
        canMatch: [authGuard],
        loadComponent: () =>
          import('./features/datasets/pages/my-datasets/my-datasets').then((m) => m.MyDatasets),
      },
      {
        path: 'create-dataset',
        canMatch: [authGuard],
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

  // ------------------- ADMIN ------------------------

  {
    path: 'admin',
    canMatch: [adminGuard, authGuard],
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'experiments' },
      {
        path: 'experiments',
        loadComponent: () =>
          import('./features/admin/experiments').then((m) => m.AllExperimentsPage),
      },
      {
        path: 'templates',
        loadComponent: () => import('./features/admin/templates').then((m) => m.AllTemplatesPage),
      },
      {
        path: 'pending',
        loadComponent: () =>
          import('./features/admin/templates-pending').then((m) => m.PendingTemplatesPage),
      },
    ],
  },

  { path: '**', redirectTo: 'docs/about' },
];
