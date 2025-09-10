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
import { ConfirmPopupInput, ConfirmPopupResponse } from 'src/app/models/popup';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmPopupComponent } from '../../general/popup/confirm-popup.component';
import { ActivatedRoute, Router } from '@angular/router';


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

  constructor(
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private router: Router,
    private dialog: MatDialog,
    private route: ActivatedRoute,
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
          value: env.value,
          is_secret: env.is_secret
        });
      }
      else if (optEnvironmentVarNames.includes(env.key)) {
        tableData.push({
          key: env.key,
          value: env.value,
          is_secret: env.is_secret
        });
      }
    }

    return tableData;
  }

  onCreateRun(): void {
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
    firstValueFrom(this.backend.getExperimentRunsCount(this.experiment.id))
      .then(count => {
        let existRuns = count > 0;
        let routeParts = ['update'];
        let routeExtras = {
          relativeTo: this.route,
        };

        if (existRuns) {
          let str = (
            "This Experiment is already associated with some experiment runs. " +
            "Modifying parameters that could change the experiment's behavior is restricted."
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
              if (state == ConfirmPopupResponse.Yes) {
                this.router.navigate(routeParts, routeExtras);
              }
            });
        }
        else {
          this.router.navigate(routeParts, routeExtras);
        }
      })
      .catch(err => console.error(err));
  }

  deleteBtnClicked(): void {
    firstValueFrom(this.backend.getExperimentRunsCount(this.experiment.id))
      .then(count => {
        let existRuns = count > 0;
        let routeParts = ["/experiments", "my"];

        let str = (
          existRuns
          ?
          "This Experiment is already associated with some experiment runs. " +
          "You can either DELETE this experiment with all its Experiment Runs " +
          "or ARCHIVE this experiment making execution of new runs not possible " +
          "whilst keeping the previously executed runs intact.\n\n" +
          "What operation do you wish to perform?"
          :
          "Do you wish to DELETE this experiment?"
        );
        let acceptStr = existRuns ? "Delete experiment and all its runs" : "Yes";
        let declineStr = existRuns ? "Dismiss" : "No";
        let thirdOptStr = existRuns ? "Archive experiment" : "";

        let popupInput: ConfirmPopupInput = {
          message: str,
          acceptBtnMessage: acceptStr,
          declineBtnMessage: declineStr,
          thirdOptionBtnMessage: thirdOptStr
        }

        firstValueFrom(this.dialog.open(ConfirmPopupComponent, {
          maxWidth: existRuns ? '600px' : '450px',
          width: '100%',
          autoFocus: false,
          data: popupInput
        }).afterClosed())
          .then(state => {
            if (state == ConfirmPopupResponse.Yes) {
              firstValueFrom(this.backend.deleteExperiment(this.experiment.id))
                .then(_ => this.router.navigate(routeParts))
                .catch(err => console.error(err));
            }
            else if (state == ConfirmPopupResponse.ThirdOption) {
              firstValueFrom(this.backend.archiveExperiment(this.experiment.id, true))
                .then(_ => this.router.navigate(routeParts))
                .catch(err => console.error(err));
            }
          });
      })
      .catch(err => console.error(err));
  }

  undoBtnClicked(): void {
   firstValueFrom(this.backend.archiveExperiment(this.experiment.id, false))
    .then(_ => {
      this.experiment.is_mine = true;
      this.experiment.is_archived = false;
    })
    .catch(err => console.error(err));
  }
}
