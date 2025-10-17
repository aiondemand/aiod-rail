import {
  Component,
  DestroyRef,
  OnInit,
  computed,
  inject,
  signal,
  Inject,
  PLATFORM_ID,
} from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map, switchMap, startWith, distinctUntilChanged, filter } from 'rxjs/operators';
import { interval, fromEvent, merge, of } from 'rxjs';

import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import {
  UiConfirmComponent,
  UiConfirmData,
  UiConfirmResult,
} from '../../../../shared/components/ui-confirm/ui-confirm';
import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';
import { UiCodeBlock } from '../../../../shared/components/ui-code-block/ui-code-block';
import { UiButton } from '../../../../shared/components/ui-button/ui-button';

import { ExperimentTemplate } from '../../../../shared/models/experiment-template';
import { EnvironmentVarDef } from '../../../../shared/models/env-vars';

import { AuthService } from '../../../../core/auth/auth.service';

@Component({
  selector: 'app-template-detail',
  standalone: true,
  imports: [
    CommonModule,
    UiLoadingComponent,
    UiErrorComponent,
    UiCodeBlock,
    UiButton,
    MatIconModule,
    MatTooltipModule,
    MatDialogModule,
  ],
  templateUrl: './template-detail.html',
  styleUrls: ['./template-detail.scss'],
})
export class TemplateDetailPage implements OnInit {
  // DI
  private api = inject(BackendApiService);
  private dialog = inject(MatDialog);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private auth = inject(AuthService);
  private destroyRef = inject(DestroyRef);
  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  // SSR guard
  private get isBrowser() {
    return isPlatformBrowser(this.platformId);
  }
  private get isDocVisible(): boolean {
    return this.isBrowser && typeof document !== 'undefined'
      ? document.visibilityState === 'visible'
      : false;
  }

  // ----- state
  id = signal<string>('');
  tpl = signal<ExperimentTemplate | null>(null);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  // ----- derived
  isMine = computed(() => this.tpl()?.is_mine ?? false);
  isArchived = computed(() => this.tpl()?.is_archived ?? false);
  isApproved = computed(() => this.tpl()?.is_approved ?? false);
  isPublic = computed(() => this.tpl()?.is_public ?? false);
  isAdminUser = computed(() => this.auth.isLoggedIn() && this.auth.hasAdminRole());
  state = computed(() => (this.tpl()?.state ?? '') as string);

  isFinished = computed(() => this.state() === 'FINISHED');
  isCreated = computed(() => this.state() === 'CREATED');
  isInProgress = computed(() => this.state() === 'IN_PROGRESS');
  isCrashed = computed(() => this.state() === 'CRASHED');

  requiredEnvs = computed<EnvironmentVarDef[]>(
    () => (this.tpl()?.envs_required ?? []) as EnvironmentVarDef[]
  );
  optionalEnvs = computed<EnvironmentVarDef[]>(
    () => (this.tpl()?.envs_optional ?? []) as EnvironmentVarDef[]
  );
  hasNoEnvs = computed(() => {
    const t = this.tpl();
    return !t || ((t.envs_required?.length ?? 0) === 0 && (t.envs_optional?.length ?? 0) === 0);
  });

  // ----- lifecycle
  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        map((pm) => pm.get('id') ?? ''),
        distinctUntilChanged(),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((id) => {
        this.id.set(id);
        this.loadOnce();
      });

    // LIVE UPDATE
    if (this.isBrowser) {
      const visibility$ = merge(fromEvent(document, 'visibilitychange'), of(null)).pipe(
        map(() => this.isDocVisible),
        startWith(this.isDocVisible),
        distinctUntilChanged()
      );

      interval(5000)
        .pipe(
          startWith(0),
          switchMap(() => visibility$),
          filter((visible) => visible),
          switchMap(() => {
            const id = this.id();
            const shouldPoll =
              !!id && !this.isArchived() && (!this.isFinished() || !this.isApproved());

            if (!shouldPoll) return of(null);
            return this.api.getExperimentTemplate(id);
          }),
          takeUntilDestroyed(this.destroyRef)
        )
        .subscribe({
          next: (t) => {
            if (!t) return;

            this.tpl.set(t);
          },
          error: (err) => console.error('[TemplateDetail] poll error', err),
        });
    }
  }

  // ----- data
  private loadOnce() {
    const id = this.id();
    if (!id) return;

    this.loading.set(true);
    this.error.set(null);

    this.api
      .getExperimentTemplate(id)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (t) => {
          this.tpl.set(t);
          // fix NG0100 pri SSR/hydration
          queueMicrotask(() => this.loading.set(false));
        },
        error: (err) => {
          console.error('[TemplateDetail] loadOnce ERROR', err);
          queueMicrotask(() =>
            this.error.set(err?.error?.message || err?.message || 'Failed to load template detail.')
          );
          queueMicrotask(() => this.loading.set(false));
        },
      });
  }

  retry() {
    this.loadOnce();
  }

  // ----- actions
  approve() {
    if (!this.isAdminUser()) {
      console.warn('[TemplateDetail] approve aborted: not admin');
      return;
    }

    const t = this.tpl();
    if (!t) {
      console.warn('[TemplateDetail] approve aborted: tpl null');
      return;
    }

    const data: UiConfirmData = {
      message:
        'Approve this template for use?\n\nApproved templates may be used to create experiments.',
      acceptBtnMessage: 'Approve',
      declineBtnMessage: 'Cancel',
    };

    const ref = this.dialog.open(UiConfirmComponent, {
      maxWidth: '450px',
      width: '100%',
      data,
    });

    ref.afterClosed().subscribe((res: UiConfirmResult | undefined) => {
      if (res !== 'yes') return;

      this.api
        .approveExperimentTemplate(t.id, true)
        .pipe(takeUntilDestroyed(this.destroyRef))
        .subscribe({
          next: () => {
            this.tpl.update((x) => (x ? { ...x, is_approved: true } : x));
          },
          error: (err) => console.error('[TemplateDetail] approve API ERROR', err),
        });
    });
  }

  edit() {
    const id = this.id();
    if (!id) return;

    this.api
      .getExperimentsOfTemplateCount(id, false)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (count) => {
          const exists = (count ?? 0) > 0;

          // v edit()
          if (exists) {
            const data: UiConfirmData = {
              message:
                'This template is already used by at least one experiment. Editing parameters that change behavior is restricted.',
              acceptBtnMessage: 'Continue',
              declineBtnMessage: 'Cancel',
            };
            this.dialog
              .open(UiConfirmComponent, {
                maxWidth: '450px',
                width: '100%',
                data,
              })
              .afterClosed()
              .subscribe((res: UiConfirmResult | undefined) => {
                if (res === 'yes') {
                  this.router.navigate(['update'], { relativeTo: this.route });
                }
              });
          } else {
            this.router.navigate(['update'], { relativeTo: this.route });
          }
        },
        error: (err) => console.error('[TemplateDetail] edit count ERROR', err),
      });
  }

  deleteOrArchive() {
    const t = this.tpl();
    if (!t) return;

    this.api
      .getExperimentsOfTemplateCount(t.id, false)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (count) => {
          const exists = (count ?? 0) > 0;

          const msg = exists
            ? 'This template is already used by some experiment. You cannot delete it, but you can archive it to prevent creating new experiments from it.\n\nDo you wish to ARCHIVE this experiment template?'
            : 'Do you wish to DELETE this experiment template?';

          const data: UiConfirmData = {
            message: msg,
            acceptBtnMessage: 'Yes',
            declineBtnMessage: 'No',
          };

          this.dialog
            .open(UiConfirmComponent, { maxWidth: '450px', width: '100%', data })
            .afterClosed()
            .subscribe((res: UiConfirmResult | undefined) => {
              if (res !== 'yes') return;

              if (exists) {
                this.api
                  .archiveExperimentTemplate(t.id, true)
                  .pipe(takeUntilDestroyed(this.destroyRef))
                  .subscribe({
                    next: () => {
                      this.router.navigate(['/experiments/templates']);
                    },
                    error: (err) => console.error('[TemplateDetail] archive API ERROR', err),
                  });
              } else {
                this.api
                  .deleteExperimentTemplate(t.id)
                  .pipe(takeUntilDestroyed(this.destroyRef))
                  .subscribe({
                    next: () => {
                      this.router.navigate(['/experiments/templates']);
                    },
                    error: (err) => console.error('[TemplateDetail] delete API ERROR', err),
                  });
              }
            });
        },
        error: (err) => console.error('[TemplateDetail] delete/archive count ERROR', err),
      });
  }

  unarchive() {
    const t = this.tpl();
    if (!t) return;

    this.api
      .archiveExperimentTemplate(t.id, false)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.tpl.update((x) => (x ? { ...x, is_archived: false, is_mine: true } : x));
        },
        error: (err) => console.error('[TemplateDetail] unarchive API ERROR', err),
      });
  }

  // ----- helpers
  file(text?: string | null) {
    return text ?? '';
  }
}
