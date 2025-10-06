import { Component, DestroyRef, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map } from 'rxjs/operators';

import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog } from '@angular/material/dialog';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { UiConfirmComponent } from '../../../../shared/components/ui-confirm/ui-confirm';
import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';
import { UiCodeBlock } from '../../../../shared/components/ui-code-block/ui-code-block';
import { UiButton } from '../../../../shared/components/ui-button/ui-button';

import { ConfirmPopupInput, ConfirmPopupResponse } from '../../../../shared/models/popup';
import { ExperimentTemplate } from '../../../../shared/models/experiment-template';
import { EnvironmentVarDef } from '../../../../shared/models/env-vars';

@Component({
  selector: 'app-template-detail',
  standalone: true,
  imports: [
    CommonModule,

    // UI
    UiLoadingComponent,
    UiErrorComponent,
    UiCodeBlock,
    UiButton,

    // Material
    MatIconModule,
    MatTooltipModule,
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
  private destroyRef = inject(DestroyRef);

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
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((id) => {
        this.id.set(id);
        this.load();
      });
  }

  // ----- data
  private load() {
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
          this.loading.set(false);
        },
        error: (err) => {
          console.error(err);
          this.error.set(err?.error?.message || err?.message || 'Failed to load template detail.');
          this.loading.set(false);
        },
      });
  }

  retry() {
    this.load();
  }

  // ----- actions
  approve() {
    const t = this.tpl();
    if (!t) return;

    this.api
      .approveExperimentTemplate(t.id, true)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => this.tpl.update((x) => (x ? { ...x, is_approved: true } : x)),
        error: (err) => console.error(err),
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

          if (exists) {
            const data: ConfirmPopupInput = {
              message:
                'This template is already used by at least one experiment. Editing parameters that change behavior is restricted.',
              acceptBtnMessage: 'Continue',
            };
            this.dialog
              .open(UiConfirmComponent, {
                maxWidth: '450px',
                width: '100%',
                autoFocus: false,
                data,
              })
              .afterClosed()
              .subscribe((res: ConfirmPopupResponse) => {
                if (res === ConfirmPopupResponse.Yes) {
                  this.router.navigate(['../', id, 'update'], { relativeTo: this.route });
                }
              });
          } else {
            this.router.navigate(['../', id, 'update'], { relativeTo: this.route });
          }
        },
        error: (err) => console.error(err),
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

          const data: ConfirmPopupInput = {
            message: msg,
            acceptBtnMessage: 'Yes',
            declineBtnMessage: 'No',
          };

          this.dialog
            .open(UiConfirmComponent, { maxWidth: '450px', width: '100%', autoFocus: false, data })
            .afterClosed()
            .subscribe((res: ConfirmPopupResponse) => {
              if (res !== ConfirmPopupResponse.Yes) return;

              if (exists) {
                this.api
                  .archiveExperimentTemplate(t.id, true)
                  .pipe(takeUntilDestroyed(this.destroyRef))
                  .subscribe({
                    next: () => this.router.navigate(['/experiments/templates']),
                    error: (err) => console.error(err),
                  });
              } else {
                this.api
                  .deleteExperimentTemplate(t.id)
                  .pipe(takeUntilDestroyed(this.destroyRef))
                  .subscribe({
                    next: () => this.router.navigate(['/experiments/templates']),
                    error: (err) => console.error(err),
                  });
              }
            });
        },
        error: (err) => console.error(err),
      });
  }

  unarchive() {
    const t = this.tpl();
    if (!t) return;

    this.api
      .archiveExperimentTemplate(t.id, false)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => this.tpl.update((x) => (x ? { ...x, is_archived: false, is_mine: true } : x)),
        error: (err) => console.error(err),
      });
  }

  // ----- helpers
  file(text?: string | null) {
    return text ?? '';
  }
}
