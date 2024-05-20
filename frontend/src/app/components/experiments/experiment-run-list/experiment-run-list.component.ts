import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { Observable, catchError, firstValueFrom, map, of } from 'rxjs';
import { Experiment } from 'src/app/models/experiment';
import { ExperimentRun } from 'src/app/models/experiment-run';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { MatSort } from '@angular/material/sort';
import { ConfirmPopupInput, ConfirmPopupResponse } from 'src/app/models/popup';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmPopupComponent } from '../../general/popup/confirm-popup.component';

@Component({
  selector: 'app-experiment-run-list',
  templateUrl: './experiment-run-list.component.html',
  styleUrls: ['./experiment-run-list.component.scss']
})
export class ExperimentRunListComponent implements OnInit {
  @ViewChild(MatSort) sort: MatSort;
  
  @Input() experiment: Experiment;

  runs$: Observable<ExperimentRun[]>;
  error: string = '';

  displayedColumns = ['id', 'state', 'created_at', 'updated_at', 'metrics', 'actions']

  constructor(
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private dialog: MatDialog,
  ) { }

  // TODO make this table dynamically reflect the current state of experiment runs
  ngOnInit(): void {
    this.updateRuns();
  }

  updateRuns(): void {
    this.runs$ = this.backend.getExperimentRuns(this.experiment.id)
      .pipe(
        map(runs => runs.sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at))),
        catchError(err => {
          this.error = `Couldn't load experiment runs: ${err.message}}`;
          this.snackBar.showError("Couldn't load experiment runs.");
          return of([]);
        })
      );
  }

  stopRun(id: string): void {
    // TODO for now we disable the ability to stop a run 
    // TODO later on we can enable this functionality again once we can
    // stop the experiment run whenever during the experiment run execution pipeline
    let popupInput: ConfirmPopupInput = {
      message: "Do you wish to stop this run?",
      acceptBtnMessage: "Yes",
      declineBtnMessage: "No",
    }
    firstValueFrom(this.dialog.open(ConfirmPopupComponent, {
      maxWidth: '450px',
      width: '100%',
      autoFocus: false,
      data: popupInput
    }).afterClosed())
      .then(state => {
        if (state == ConfirmPopupResponse.Yes) {
          firstValueFrom(this.backend.stopExperimentRun(id))
            .then(_ => this.updateRuns())
            .catch(err => console.error(err));
        }
      });
  }

  deleteRun(id: string): void {
    // TODO for now we can delete run only when its finished/crashed
    // TODO later on also allow the option to delete it mid execution
    let popupInput: ConfirmPopupInput = {
      message: "Do you wish to delete this run?",
      acceptBtnMessage: "Yes",
      declineBtnMessage: "No",
    }
    firstValueFrom(this.dialog.open(ConfirmPopupComponent, {
      maxWidth: '450px',
      width: '100%',
      autoFocus: false,
      data: popupInput
    }).afterClosed())
      .then(state => {
        if (state == ConfirmPopupResponse.Yes) {
          firstValueFrom(this.backend.deleteExperimentRun(id))
            .then(_ => this.updateRuns())
            .catch(err => console.error(err));
        }
      });
  }
}
