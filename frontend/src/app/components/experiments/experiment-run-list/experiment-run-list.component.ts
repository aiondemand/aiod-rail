import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { Observable, catchError, map, of } from 'rxjs';
import { Experiment } from 'src/app/models/experiment';
import { ExperimentRun } from 'src/app/models/experiment-run';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { MatSort } from '@angular/material/sort';

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
    private snackBar: SnackBarService
  ) { }

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
}
