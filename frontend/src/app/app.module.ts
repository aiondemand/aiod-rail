import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { HttpClientModule } from '@angular/common/http';
import { MatTabsModule } from '@angular/material/tabs';
import { ExperimentsComponent } from './components/experiments/experiments.component';
import { DatasetsComponent } from './components/datasets/datasets.component';
import { PublicationsComponent } from './components/publications/publications.component';
import { MatGridListModule } from '@angular/material/grid-list';
import { DatasetListComponent } from './components/datasets/dataset-list/dataset-list.component';
import { DatasetDetailComponent } from './components/datasets/dataset-detail/dataset-detail.component';
import { MatCardModule } from '@angular/material/card';
import { MatExpansionModule } from '@angular/material/expansion';
import { DatasetListItemComponent } from './components/datasets/dataset-list-item/dataset-list-item.component';
import { EllipsisPipe } from './pipes/ellipsis.pipe';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatChipsModule } from '@angular/material/chips';
import { DefaultIfEmptyPipe } from './pipes/default-if-empty.pipe';
import { MarkdownModule } from 'ngx-markdown';
import { MatTooltipModule } from '@angular/material/tooltip';
import { SavedDatasetsComponent } from './components/datasets/saved-datasets/saved-datasets.component';
import { SaveRemoveDatasetButtonComponent } from './components/datasets/utils/save-remove-dataset-button/save-remove-dataset-button.component';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { OAuthModule, OAuthStorage } from 'angular-oauth2-oidc';
import { LoginLogoutComponent } from './authorization/login-logout/login-logout.component';
import { environment } from 'src/environments/environment';
import { CreateDatasetComponent } from './components/datasets/create-dataset/create-dataset.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { TextFieldModule } from '@angular/cdk/text-field';
import { HuggingfaceFormComponent } from './components/datasets/create-dataset/huggingface-form/huggingface-form.component';
import { FormatPlatformNamePipe } from './pipes/format-platform-name.pipe';
import { CreateExperimentComponent } from './components/experiments/create-experiment/create-experiment.component';
import { ExperimentDetailComponent } from './components/experiments/experiment-detail/experiment-detail.component';
import { ExperimentListItemComponent } from './components/experiments/experiment-list-item/experiment-list-item.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { ExperimentRunListComponent } from './components/experiments/experiment-run-list/experiment-run-list.component';
import { ExperimentRunDetailComponent } from './components/experiments/experiment-run-detail/experiment-run-detail.component';
import { MatTableModule } from '@angular/material/table';
import { AllExperimentListComponent } from './components/experiments/experiment-lists/all-experiment-list.component';
import { MyExperimentListComponent } from './components/experiments/experiment-lists/my-experiment-list.component';
import { AllExperimentTemplateList } from './components/experiments/experiment-template-lists/all-experiment-template-list.component';
import { MyExperimentTemplateList } from './components/experiments/experiment-template-lists/my-experiment-template-list.component';
import { ExperimentTemplateListItemComponent } from './components/experiments/experiment-template-list-item/experiment-template-list-item.component';
import { ExperimentTemplateDetailComponent } from './components/experiments/experiment-template-detail/experiment-template-detail.component';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { HIGHLIGHT_OPTIONS, HighlightModule, HighlightOptions } from 'ngx-highlightjs';
import { CodeEditorModule } from '@ngstack/code-editor';
import { FeedbackComponent } from './components/general/feedback/feedback.component';
import { AboutComponent } from './components/general/about/about.component';
import { NgOptimizedImage } from "@angular/common";
import { MatTreeModule } from '@angular/material/tree';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { EditExperimentTemplateComponent } from './components/experiments/edit-experiment-template/edit-experiment-template.component';
import { UpdateExperimentComponent } from './components/experiments/update-experiment/update-experiment.component';




@NgModule({
  declarations: [
    AppComponent,
    ExperimentsComponent,
    DatasetsComponent,
    PublicationsComponent,
    DatasetListComponent,
    DatasetDetailComponent,
    DatasetListItemComponent,
    EllipsisPipe,
    DefaultIfEmptyPipe,
    SavedDatasetsComponent,
    SaveRemoveDatasetButtonComponent,
    CreateDatasetComponent,
    HuggingfaceFormComponent,
    LoginLogoutComponent,
    FormatPlatformNamePipe,
    CreateExperimentComponent,
    ExperimentDetailComponent,
    ExperimentListItemComponent,
    ExperimentRunListComponent,
    ExperimentRunDetailComponent,
    MyExperimentListComponent,
    AllExperimentListComponent,
    AllExperimentTemplateList,
    MyExperimentTemplateList,
    ExperimentTemplateListItemComponent,
    ExperimentTemplateDetailComponent,
    FeedbackComponent,
    AboutComponent,
    EditExperimentTemplateComponent,
    UpdateExperimentComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatButtonModule,
    MatTabsModule,
    MatGridListModule,
    MatCardModule,
    MatExpansionModule,
    MatPaginatorModule,
    MatChipsModule,
    MatTooltipModule,
    MatSnackBarModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatCheckboxModule,
    TextFieldModule,
    MatAutocompleteModule,
    HighlightModule,
    MatTreeModule,
    MatProgressBarModule,
    MarkdownModule.forRoot(),
    CodeEditorModule.forRoot(),
    OAuthModule.forRoot({
      resourceServer: {
        allowedUrls: [environment.BACKEND_API_URL],
        sendAccessToken: true
      }
    }),
    NgOptimizedImage
  ],
  providers: [
    { provide: OAuthStorage, useFactory: () => localStorage },
    {
      provide: HIGHLIGHT_OPTIONS,
      useValue: <HighlightOptions>{
        lineNumbers: true,
        coreLibraryLoader: () => import('highlight.js/lib/core'),
        lineNumbersLoader: () => import('ngx-highlightjs/line-numbers'),
        languages: {
          python: () => import('highlight.js/lib/languages/python'),
          dockerfile: () => import('highlight.js/lib/languages/dockerfile'),
          bash: () => import('highlight.js/lib/languages/bash')
        }
      }
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
