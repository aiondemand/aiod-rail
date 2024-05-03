import { Component, Input, ViewChild } from '@angular/core';
import { catchError, combineLatest, firstValueFrom, of, retry, switchMap, tap } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { Experiment } from 'src/app/models/experiment';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { Model } from 'src/app/models/model';
import { Publication } from 'src/app/models/publication';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { ExperimentRunListComponent } from '../experiment-run-list/experiment-run-list.component';
import { EnvironmentVar } from 'src/app/models/env-vars';



@Component({
  selector: 'app-experiment-detail',
  templateUrl: './experiment-detail.component.html',
  styleUrls: ['./experiment-detail.component.scss']
})
export class ExperimentDetailComponent {
  @ViewChild('runList') runListComponent: ExperimentRunListComponent;

  experiment: Experiment;
  dataset: Dataset;
  model: Model;
  relatedPublications: Publication[] = [];
  experimentTemplate: ExperimentTemplate;

  constructor(private backend: BackendApiService, private snackBar: SnackBarService) { }

  displayedEnvVarColumns: string[] = ['key', 'value'];
  envTableData: EnvironmentVar[] | null = null;


  @Input()
  set id(id: string) {
    // get experiment by id from backend. Then, get ExperimentTemplate from the backend, using experiment.experiment_type_id

    var data$ = this.backend.getExperiment(id)
      .pipe(
        switchMap(experiment => combineLatest([
          // TODO: Update to use arrays
          this.backend.getDataset(experiment.dataset_ids[0]),
          this.backend.getModel(experiment.model_ids[0]),
          this.backend.getExperimentPublications(experiment),
          this.backend.getExperimentTemplate(experiment.experiment_template_id),
          of(experiment)
        ])),
        retry(3)
      );

    firstValueFrom(data$)
      .then(([dataset, model, publications, experimentTemplate, experiment]) => {
        this.dataset = dataset;
        this.model = model;
        this.relatedPublications = publications;
        this.experimentTemplate = experimentTemplate;
        this.experiment = experiment;

        this.envTableData = this.buildEnvTable();
      })
      .catch(err => {
        this.snackBar.showError("Failed to load experiment details");
      });
  }

  buildEnvTable(): EnvironmentVar[] {
    let tableData: EnvironmentVar[] = [];

    let reqEnvironmentVarNames = this.experimentTemplate.envs_required.map(env => env.name);
    let optEnvironmentVarNames = this.experimentTemplate.envs_optional.map(env => env.name);

    for (let env of this.experiment.env_vars) {
      if (reqEnvironmentVarNames.includes(env.key)) {
        tableData.push({
          key: `${env.key}*`,
          value: env.value
        });
      }
      else if (optEnvironmentVarNames.includes(env.key)) {
        tableData.push({
          key: env.key,
          value: env.value
        });
      }
    }

    return tableData;
  }

  onCreateRun() {
    // // filter out envs that are empty
    // const nonEmptyEnvs: { [key: string]: string } = {};
    // for (const key in this.envs) {
    //   if (this.envs[key] !== '') {
    //     nonEmptyEnvs[key] = this.envs[key];
    //   }
    // }

    firstValueFrom(
      this.backend.executeExperimentRun(this.experiment.id)
        .pipe(
          catchError(err => {
            if (err.status == 401) {
              this.snackBar.showError("An authorization error occurred. Try logging out and then logging in again.");
            }
            else if (err.status == 500) {
              this.snackBar.showError(`Failed to create run: ${err.message}. ${err.error.detail}`);
            }
            else {
              this.snackBar.showError(`Failed to create run: ${err}`);
            }
            return [];
          })
        )
      )
        .then(run => {
          this.snackBar.show(`Created run ${run.id}`);
          this.runListComponent.updateRuns();
        });
  }
}
