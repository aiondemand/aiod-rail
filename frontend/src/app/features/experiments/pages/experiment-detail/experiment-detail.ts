import {
  Component,
  DestroyRef,
  Injector,
  OnInit,
  ViewChild,
  inject,
  signal,
  computed,
} from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { combineLatest, of, fromEvent, interval, EMPTY } from 'rxjs';
import { switchMap, retry, first, map, catchError, startWith } from 'rxjs/operators';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { UiButton } from '../../../../shared/components/ui-button/ui-button';
import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';

import { Experiment } from '../../../../shared/models/experiment';
import { Dataset } from '../../../../shared/models/dataset';
import { Model } from '../../../../shared/models/model';
import { ExperimentTemplate } from '../../../../shared/models/experiment-template';
import { Publication } from '../../../../shared/models/publication';

import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import {
  UiConfirmComponent,
  UiConfirmData,
  UiConfirmResult,
} from '../../../../shared/components/ui-confirm/ui-confirm';

import { ExperimentRunListComponent } from '../../../../shared/components/experiment-run-list/experiment-run-list';

@Component({
  selector: 'app-experiment-detail',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    DatePipe,
    MatIconModule,
    MatTooltipModule,
    UiButton,
    UiLoadingComponent,
    UiErrorComponent,
    MatDialogModule,
    ExperimentRunListComponent,
  ],
  templateUrl: './experiment-detail.html',
  styleUrls: ['./experiment-detail.scss'],
})
export class ExperimentDetailPage implements OnInit {
  private api = inject(BackendApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);
  private injector = inject(Injector);
  private dialog = inject(MatDialog);

  @ViewChild('runList') runListComponent?: any;

  // state
  experiment = signal<Experiment | null>(null);
  dataset = signal<Dataset | null>(null);
  model = signal<Model | null>(null);
  tpl = signal<ExperimentTemplate | null>(null);
  publications = signal<Publication[]>([]);

  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  // computed
  isPublic = computed(() => !!(this.experiment() as any)?.is_public);
  isMine = computed(() => !!(this.experiment() as any)?.is_mine);
  isArchived = computed(() => !!(this.experiment() as any)?.is_archived);

  title = computed(() => (this.experiment() as any)?.name ?? 'Experiment');
  createdAt = computed(() => (this.experiment() as any)?.created_at ?? null);
  updatedAt = computed(() => (this.experiment() as any)?.updated_at ?? null);
  id = computed(() => (this.experiment() as any)?.id ?? '');

  totalRunCount = signal<number>(0);

  canCreateRun = computed(() => this.isMine() && !this.isArchived());

  envRows = computed(() => {
    const e = this.experiment();
    const t = this.tpl();
    if (!e || !t) return [];

    const req = (t as any).envs_required?.map((x: any) => x?.name) ?? [];
    const opt = (t as any).envs_optional?.map((x: any) => x?.name) ?? [];
    const fromExp: Array<{ key: string; value: string; is_secret?: boolean }> =
      (e as any).env_vars ?? [];

    const rows: Array<{ key: string; value: string; is_secret?: boolean; required: boolean }> = [];
    for (const env of fromExp) {
      const required = req.includes(env.key);
      if (required || opt.includes(env.key)) {
        rows.push({
          key: required ? `${env.key}*` : env.key,
          value: env.value,
          is_secret: env.is_secret,
          required,
        });
      }
    }
    return rows;
  });

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        switchMap((pm) => {
          const id = pm.get('id');
          if (!id) {
            this.error.set('Missing experiment ID.');
            return of(null);
          }
          this.loading.set(true);
          this.error.set(null);

          return this.api.getExperiment(id).pipe(
            switchMap((exp) =>
              combineLatest([
                of(exp),
                exp?.dataset_ids?.length ? this.api.getDataset(exp.dataset_ids[0]) : of(null),
                exp?.model_ids?.length ? this.api.getModel(exp.model_ids[0]) : of(null),
                this.api.getExperimentPublications(exp),
                exp?.experiment_template_id
                  ? this.api.getExperimentTemplate(exp.experiment_template_id)
                  : of(null),
              ])
            ),
            retry(2)
          );
        })
      )
      .subscribe({
        next: (tuple) => {
          if (!tuple) return;
          const [exp, ds, mdl, pubs, tpl] = tuple;
          this.experiment.set(exp ?? null);
          this.dataset.set(ds ?? null);
          this.model.set(mdl ?? null);
          this.publications.set(pubs ?? []);
          this.tpl.set(tpl ?? null);
          this.loading.set(false);

          this.refreshTotalRunCount();
          this.startAutoCountRefresh();
        },
        error: (err: any) => {
          console.error(err);
          this.error.set(err?.error?.message || err?.message || 'Failed to load experiment.');
          this.loading.set(false);
        },
      });
  }

  onRunsChanged() {
    this.refreshTotalRunCount();
  }

  private refreshTotalRunCount(): void {
    const exp = this.experiment();
    if (!exp) return;

    const hasCount = !!this.api.getExperimentRunsCount;
    if (hasCount) {
      this.api
        .getExperimentRunsCount((exp as any).id)
        .pipe(
          first(),
          catchError(() => of(0))
        )
        .subscribe((cnt: number) => this.totalRunCount.set(cnt || 0));
      return;
    }

    // fallback
    this.api
      .getExperimentRuns((exp as any).id)
      .pipe(
        first(),
        map((list: any[]) => (list ?? []).length),
        catchError(() => of(0))
      )
      .subscribe((cnt) => this.totalRunCount.set(cnt));
  }

  /** refresh every 10 sec if (count > 0). */
  private startAutoCountRefresh(): void {
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
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe(() => {
        if (this.totalRunCount() === 0) return;
        this.refreshTotalRunCount();
      });
  }

  /** create new run  */
  createRun(): void {
    const expId = this.id();
    if (!expId) return;

    if (!this.canCreateRun()) return;

    this.api
      .executeExperimentRun(expId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.runListComponent?.updateRuns?.();
          this.refreshTotalRunCount();
        },
        error: (err) => {
          const data: UiConfirmData = {
            message: err?.error?.message || 'Failed to start run.',
            acceptBtnMessage: 'OK',
            declineBtnMessage: 'Close',
          };
          this.dialog.open(UiConfirmComponent, { width: '100%', maxWidth: '520px', data });
        },
      });
  }

  goEdit() {
    const exp = this.experiment();
    if (!exp) return;

    this.api
      .getExperimentRunsCount((exp as any).id)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (count: number) => {
          if (count > 0) {
            const data: UiConfirmData = {
              message:
                'This Experiment is already associated with some experiment runs.\n' +
                "Modifying parameters that could change the experiment's behavior is restricted.",
              acceptBtnMessage: 'Continue',
              declineBtnMessage: 'Cancel',
            };
            this.dialog
              .open(UiConfirmComponent, {
                width: '100%',
                maxWidth: '480px',
                data,
              })
              .afterClosed()
              .subscribe((res: UiConfirmResult) => {
                if (res === 'yes') {
                  this.router.navigate(['update'], { relativeTo: this.route });
                }
              });
          } else {
            this.router.navigate(['update'], { relativeTo: this.route });
          }
        },
        error: (err) => console.error(err),
      });
  }

  doDelete() {
    const exp = this.experiment();
    if (!exp) return;
    const expId = (exp as any).id;

    this.api
      .getExperimentRunsCount(expId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (count: number) => {
          const existRuns = count > 0;

          const data: UiConfirmData = existRuns
            ? {
                message:
                  'This Experiment is already associated with some experiment runs.\n' +
                  'You can either DELETE this experiment with all its Experiment Runs ' +
                  'or ARCHIVE this experiment making execution of new runs not possible ' +
                  'whilst keeping the previously executed runs intact.\n\n' +
                  'What operation do you wish to perform?',
                acceptBtnMessage: 'Delete experiment and all its runs',
                declineBtnMessage: 'Dismiss',
                thirdOptionBtnMessage: 'Archive experiment',
              }
            : {
                message: 'Do you wish to DELETE this experiment?',
                acceptBtnMessage: 'Yes',
                declineBtnMessage: 'No',
              };

          this.dialog
            .open(UiConfirmComponent, {
              width: '100%',
              maxWidth: existRuns ? '700px' : '420px',
              data,
            })
            .afterClosed()
            .subscribe((res: UiConfirmResult) => {
              if (res === 'yes') {
                this.api
                  .deleteExperiment(expId)
                  .pipe(takeUntilDestroyed(this.destroyRef))
                  .subscribe({
                    next: () => this.router.navigate(['/experiments', 'public']),
                    error: (err) => console.error(err),
                  });
              } else if (res === 'third' && existRuns) {
                this.api
                  .archiveExperiment(expId, true)
                  .pipe(takeUntilDestroyed(this.destroyRef))
                  .subscribe({
                    next: () => {
                      const e = this.experiment();
                      if (e) {
                        this.experiment.set({ ...(e as any), is_archived: true, is_mine: true });
                      }
                    },
                    error: (err) => console.error(err),
                  });
              }
            });
        },
        error: (err) => console.error(err),
      });
  }

  unarchive() {
    const expId = this.id();
    if (!expId) return;
    this.api
      .archiveExperiment(expId, false)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          const e = this.experiment();
          if (e) {
            (e as any).is_mine = true;
            (e as any).is_archived = false;
            this.experiment.set({ ...(e as any) });
          }
          this.refreshTotalRunCount();
        },
        error: (err) => console.error(err),
      });
  }
}
