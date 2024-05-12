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
import { ConfirmPopupInput } from 'src/app/models/popup-input';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmPopupComponent } from '../../general/popup/confirm-popup.component';
import { Router } from '@angular/router';


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

  isExperimentMine: boolean = false;
  existRuns: boolean = false;

  constructor(
    private backend: BackendApiService, 
    private snackBar: SnackBarService,
    private router: Router,
    private dialog: MatDialog
  ) { }

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
          this.backend.isExperimentMine(experiment.id),
          this.backend.getExperimentRunsCount(experiment.id),
          of(experiment)
        ])),
        retry(3)
      );

    firstValueFrom(data$)
      .then(([dataset, model, publications, experimentTemplate, isExperimentMine, experimentRunsCount, experiment]) => {
        this.dataset = dataset;
        this.model = model;
        this.relatedPublications = publications;
        this.experimentTemplate = experimentTemplate;
        this.isExperimentMine = isExperimentMine;
        this.existRuns = experimentRunsCount > 0;
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

  onCreateRun(): void {
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
        })
        .catch(err => console.error(err));
  }

  editBtnClicked(): void {
    let routeParts = ['/experiments', 'edit'];
    let queryParams = {  
      id: this.experiment.id
    };
    let routeExtras = { queryParams: queryParams };

    if (this.existRuns) {
      let str = (
        "Since there exist ExperimentRuns that execute this particular experiment, " + 
        "you cannot further modify the parameters that could change the experiment behavior."
      )
      let popupInput: ConfirmPopupInput = {
        message: str,
        acceptBtnMessage: "Continue"
      };
      firstValueFrom(this.dialog.open(ConfirmPopupComponent, {
        maxWidth: '450px',
        width: '100%',
        autoFocus: false,
        data: popupInput
      }).afterClosed())
        .then(state => {
          if (state) {
            this.router.navigate(routeParts, routeExtras);
          }
        });
    }
    else {
      this.router.navigate(routeParts, routeExtras);
    }
  }

  deleteBtnClicked(): void {
    // TODO
  }
}
