import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExperimentsComponent } from './components/experiments/experiments.component';
import { DatasetsComponent } from './components/datasets/datasets.component';
import { DatasetListComponent } from './components/datasets/dataset-list/dataset-list.component';
import { DatasetDetailComponent } from './components/datasets/dataset-detail/dataset-detail.component';
import { SavedDatasetsComponent } from './components/datasets/saved-datasets/saved-datasets.component';
import { CreateDatasetComponent } from './components/datasets/create-dataset/create-dataset.component';
import { adminGuard, authGuard } from './guards/auth.guard';
import { EditExperimentComponent } from './components/experiments/edit-experiment/edit-experiment.component';
import { ExperimentDetailComponent } from './components/experiments/experiment-detail/experiment-detail.component';
import { ExperimentRunDetailComponent } from './components/experiments/experiment-run-detail/experiment-run-detail.component';
import { PublicExperimentListComponent } from './components/experiments/experiment-lists/public-experiment-list.component';
import { MyExperimentListComponent } from './components/experiments/experiment-lists/my-experiment-list.component';
import { AllExperimentListComponent } from './components/admin/experiment-list/all-experiment-list.component';
import { ExperimentTemplateDetailComponent } from './components/experiments/experiment-template-detail/experiment-template-detail.component';
import { PublicExperimentTemplateListComponent } from './components/experiments/experiment-template-lists/public-experiment-template-list.component';
import { MyExperimentTemplateListComponent } from './components/experiments/experiment-template-lists/my-experiment-template-list.component';
import { AllExperimentTemplateListComponent } from './components/admin/experiment-template-lists/all-experiment-template-list.component';
import { PendingExperimentTemplateListComponent } from './components/admin/experiment-template-lists/pending-experiment-template-list.component';
import { AboutComponent } from './components/general/about/about.component';
import { EditExperimentTemplateComponent } from './components/experiments/edit-experiment-template/edit-experiment-template.component';
import { ProfileComponent } from './components/profile/profile.component';
import { AdminComponent } from './components/admin/admin.component';
import { DocsComponent } from './docs/docs.component';
import { AboutComponent as DocsAboutComponent } from './docs/about/about.component';
import { RailSdksComponent } from './docs/rail-sdks/rail-sdks.component';
import { RailOuterSdkComponent } from './docs/rail-outer-sdk/rail-outer-sdk.component';
import { RailMainConceptsComponent } from './docs/rail-main-concepts/rail-main-concepts.component';
import { RailMainConceptsExperimentTemplateComponent } from './docs/rail-main-concepts/rail-main-concepts-experiment-template.component';
import { RailMainConceptsExperimentComponent } from './docs/rail-main-concepts/rail-main-concepts-experiment.component';
import { RailMainConceptsExperimentRunComponent } from './docs/rail-main-concepts/rail-main-concepts-experiment-run.component';
import { RailInnerSdkComponent } from './docs/rail-inner-sdk/rail-inner-sdk.component';

const routes: Routes = [
  { path: '', redirectTo: 'docs/about', pathMatch: 'full' },
  { path: 'about', component: AboutComponent },
  {
    path: 'experiments',
    component: ExperimentsComponent,
    children: [
      // experiments
      { path: '', redirectTo: 'public', pathMatch: 'full' },
      { path: 'public', component: PublicExperimentListComponent},
      { path: 'my',  component: MyExperimentListComponent, canActivate: [authGuard] },
      { path: 'create', component: EditExperimentComponent, canActivate: [authGuard] },
      // TODO check whether :ID is valid or whether a specific experiment / template actually exists
      { path: ':id', component: ExperimentDetailComponent },
      { path: ':id/update', component: EditExperimentComponent, canActivate: [authGuard] },

      // experiment runs
      { path: 'runs/:runId', component: ExperimentRunDetailComponent },

      // experiment templates
      {
        path: 'templates',
        children: [
          { path: '', redirectTo: 'public', pathMatch: 'full' },
          { path: "public", component: PublicExperimentTemplateListComponent},
          { path: "my", component: MyExperimentTemplateListComponent, canActivate: [authGuard] },
          { path: 'create', component: EditExperimentTemplateComponent, canActivate: [authGuard] },
          { path: ':id', component: ExperimentTemplateDetailComponent },
          { path: ':id/update', component: EditExperimentTemplateComponent, canActivate: [authGuard] },
        ]
      }
    ],
  },
  {
    path: 'datasets', component: DatasetsComponent,
    children: [
      { path: '', redirectTo: 'all', pathMatch: 'full' },
      { path: 'all', component: DatasetListComponent },
      { path: 'my', component: SavedDatasetsComponent, canActivate: [authGuard] },
      { path: 'create', component: CreateDatasetComponent },
      { path: ':id', component: DatasetDetailComponent }
    ]
  },
  {
    path: 'profile', component: ProfileComponent, canActivate: [authGuard]
  },
  {
    path: 'admin', component: AdminComponent, canActivate: [authGuard, adminGuard],
    children: [
      { path: '', redirectTo: 'experiments/all', pathMatch: 'full' },
      { path: 'experiments/all', component: AllExperimentListComponent },
      { path: 'experiments/templates/all', component: AllExperimentTemplateListComponent },
      { path: 'experiments/templates/pending', component: PendingExperimentTemplateListComponent },
    ]
  },
  {
    path: 'docs', component: DocsComponent,
    children: [
      { path: '', redirectTo: 'about', pathMatch: 'full' },
      { path: 'about', component: DocsAboutComponent },
      { path: 'rail-sdks', component: RailSdksComponent },
      { path: 'outer-sdk', component: RailOuterSdkComponent },
      { path: 'inner-sdk', component: RailInnerSdkComponent },
      { path: 'main-concepts', component: RailMainConceptsComponent, },
      { path: 'main-concepts-template', component: RailMainConceptsExperimentTemplateComponent },
      { path: 'main-concepts-experiment', component: RailMainConceptsExperimentComponent },
      { path: 'main-concepts-run', component: RailMainConceptsExperimentRunComponent },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    bindToComponentInputs: true,
    anchorScrolling: 'enabled',
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
