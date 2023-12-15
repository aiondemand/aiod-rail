import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExperimentsComponent } from './components/experiments/experiments.component';
import { DatasetsComponent } from './components/datasets/datasets.component';
import { PublicationsComponent } from './components/publications/publications.component';
import { DatasetListComponent } from './components/datasets/dataset-list/dataset-list.component';
import { DatasetDetailComponent } from './components/datasets/dataset-detail/dataset-detail.component';
import { SavedDatasetsComponent } from './components/datasets/saved-datasets/saved-datasets.component';
import { CreateDatasetComponent } from './components/datasets/create-dataset/create-dataset.component';
import { authGuard } from './guards/auth.guard';
import { CreateExperimentComponent } from './components/experiments/create-experiment/create-experiment.component';
import { ExperimentDetailComponent } from './components/experiments/experiment-detail/experiment-detail.component';
import { ExperimentRunDetailComponent } from './components/experiments/experiment-run-detail/experiment-run-detail.component';
import { AllExperimentListComponent } from './components/experiments/experiment-lists/all-experiment-list.component';
import { MyExperimentListComponent } from './components/experiments/experiment-lists/my-experiment-list.component';
import { ExperimentTemplateDetailComponent } from './components/experiments/experiment-template-detail/experiment-template-detail.component';
import { CreateExperimentTemplateComponent } from './components/experiments/create-experiment-template/create-experiment-template.component';
import { AllExperimentTemplateList } from './components/experiments/experiment-template-lists/all-experiment-template-list.component';
import { MyExperimentTemplateList } from './components/experiments/experiment-template-lists/my-experiment-template-list.component';
import { AboutComponent } from './components/general/about/about.component';

const routes: Routes = [
  { path: '', redirectTo: 'about', pathMatch: 'full' },
  { path: 'about', component: AboutComponent },
  {
    path: 'experiments',
    component: ExperimentsComponent,
    children: [
      // experiments
      { path: '', redirectTo: 'all', pathMatch: 'full' },
      { path: 'all', component: AllExperimentListComponent},
      { path: 'my',  component: MyExperimentListComponent, canActivate: [authGuard] },
      { path: 'create', component: CreateExperimentComponent, canActivate: [authGuard] },
      { 
        path: ':id', 
        component: ExperimentDetailComponent
      },

      // experiment runs
      { path: 'runs/:runId', component: ExperimentRunDetailComponent },
      
      // experiment templates
      {
        path: 'templates', 
        children: [
          { path: '', redirectTo: 'all', pathMatch: 'full' },
          { path: "all", component: AllExperimentTemplateList},
          { path: "my", component: MyExperimentTemplateList, canActivate: [authGuard] },
          { path: 'create', component: CreateExperimentTemplateComponent, canActivate: [authGuard] },
          { path: ':id', component: ExperimentTemplateDetailComponent }
        ]
      }
    ],
  },
  {
    path: 'datasets', component: DatasetsComponent,
    children: [
      { path: '', redirectTo: 'all', pathMatch: 'full' }, 
      { path: 'all', component: DatasetListComponent },
      { path: 'saved', component: SavedDatasetsComponent },
      { path: 'create', component: CreateDatasetComponent },
      { path: ':id', component: DatasetDetailComponent }
    ]
  },
  // { path: 'publications', component: PublicationsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { bindToComponentInputs: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
