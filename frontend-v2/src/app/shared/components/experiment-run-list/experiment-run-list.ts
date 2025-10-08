import { Component, Input, OnInit, OnDestroy, inject, signal } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import {
  catchError,
  firstValueFrom,
  of,
  interval,
  fromEvent,
  merge,
  switchMap,
  startWith,
  map,
  takeUntil,
  Subject,
  EMPTY,
} from 'rxjs';

import { BackendApiService } from '../../../shared/services/backend-api.service';
import { SnackBarService } from '../../../shared/services/snack-bar.service';
import { UiLoadingComponent } from '../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../shared/components/ui-error/ui-error';
import {
  UiConfirmComponent,
  UiConfirmData,
  UiConfirmResult,
} from '../../../shared/components/ui-confirm/ui-confirm';

import { Experiment } from '../../../shared/models/experiment';
import { ExperimentRun } from '../../../shared/models/experiment-run';

@Component({
  standalone: true,
  selector: 'app-experiment-run-list',
  imports: [
    CommonModule,
    RouterLink,
    DatePipe,
    MatIconModule,
    MatTooltipModule,
    MatDialogModule,
    UiLoadingComponent,
    UiErrorComponent,
  ],
  templateUrl: './experiment-run-list.html',
  styleUrls: ['./experiment-run-list.scss'],
})
export class ExperimentRunListComponent implements OnInit, OnDestroy {
  private api = inject(BackendApiService);
  private snack = inject(SnackBarService);
  private dialog = inject(MatDialog);

  @Input({ required: true }) experiment!: Experiment;

  runs = signal<ExperimentRun[]>([]);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  private destroy$ = new Subject<void>();
  private lastSnapshot = ''; // na zníženie zbytočných renderov

  ngOnInit(): void {
    // auto-refresh: každých 10s, ale len keď je tab viditeľný
    const visible$ =
      typeof document !== 'undefined'
        ? fromEvent(document, 'visibilitychange').pipe(
            startWith(0),
            map(() => !document.hidden)
          )
        : of(true);

    visible$
      .pipe(
        switchMap((isVisible) => (isVisible ? interval(10000).pipe(startWith(0)) : EMPTY)),
        takeUntil(this.destroy$)
      )
      .subscribe(() => this.updateRuns());
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  async updateRuns() {
    if (!this.experiment) return;

    // loading len pri prvom fetchi, aby to neblikalo pri auto-refreshoch
    const firstLoad = this.runs().length === 0;
    if (firstLoad) this.loading.set(true);
    this.error.set(null);

    try {
      const list = await firstValueFrom(
        this.api.getExperimentRuns((this.experiment as any).id).pipe(
          catchError((err) => {
            console.error(err);
            this.error.set("Couldn't load experiment runs.");
            return of([]);
          })
        )
      );

      const sorted = (list ?? [])
        .slice()
        .sort((a: any, b: any) => Date.parse(b?.created_at ?? 0) - Date.parse(a?.created_at ?? 0));

      // snapshot len kľúčových polí (mení sa len keď sa reálne zmenia dáta)
      const snapshot = JSON.stringify(
        sorted.map((r: any) => ({
          id: r.id,
          state: r.state,
          updated_at: r.updated_at,
          metrics_count: r.metrics ? Object.keys(r.metrics).length : 0,
        }))
      );

      if (snapshot !== this.lastSnapshot) {
        this.runs.set(sorted);
        this.lastSnapshot = snapshot;
      }
    } finally {
      if (firstLoad) this.loading.set(false);
    }
  }

  stopRun(id: string) {
    const data: UiConfirmData = {
      message: 'Do you wish to STOP this run?',
      acceptBtnMessage: 'Yes',
      declineBtnMessage: 'No',
    };
    this.dialog
      .open(UiConfirmComponent, { width: '100%', maxWidth: '450px', data })
      .afterClosed()
      .subscribe(async (res: UiConfirmResult) => {
        if (res !== 'yes') return;
        await firstValueFrom(this.api.stopExperimentRun(id).pipe(catchError(() => of(null))));
        this.updateRuns();
      });
  }

  deleteRun(id: string) {
    const data: UiConfirmData = {
      message: 'Do you wish to DELETE this run?',
      acceptBtnMessage: 'Yes',
      declineBtnMessage: 'No',
    };
    this.dialog
      .open(UiConfirmComponent, { width: '100%', maxWidth: '450px', data })
      .afterClosed()
      .subscribe(async (res: UiConfirmResult) => {
        if (res !== 'yes') return;
        await firstValueFrom(
          this.api.deleteExperimentRun(id).pipe(
            catchError((err) => {
              console.error(err);
              this.snack.showError('Failed to delete run');
              return of(null);
            })
          )
        );
        this.updateRuns();
      });
  }
}
