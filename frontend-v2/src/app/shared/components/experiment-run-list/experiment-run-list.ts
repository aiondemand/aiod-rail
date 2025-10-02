import { Component, DestroyRef, Input, OnInit, inject, signal } from '@angular/core';
import { CommonModule, DatePipe, NgFor, NgIf } from '@angular/common';
import { RouterLink } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { BackendApiService } from '../../../shared/services/backend-api.service';
import { UiLoadingComponent } from '../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../shared/components/ui-error/ui-error';
import { UiButton } from '../../../shared/components/ui-button/ui-button';
import { UiConfirmComponent } from '../ui-confirm/ui-confirm';

import { Experiment } from '../../../shared/models/experiment';
import { ExperimentRun } from '../../../shared/models/experiment-run';
import { ConfirmPopupInput, ConfirmPopupResponse } from '../../models/popup';

import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog } from '@angular/material/dialog';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-experiment-run-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    DatePipe,
    MatIconModule,
    MatTooltipModule,
    UiLoadingComponent,
    UiErrorComponent,
    UiButton,
  ],
  templateUrl: './experiment-run-list.html',
  styleUrls: ['./experiment-run-list.scss'],
})
export class ExperimentRunListComponent implements OnInit {
  private api = inject(BackendApiService);
  private destroyRef = inject(DestroyRef);
  private dialog = inject(MatDialog);

  @Input() experiment!: Experiment;

  runs = signal<ExperimentRun[]>([]);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  ngOnInit(): void {
    this.updateRuns();
  }

  updateRuns(): void {
    if (!this.experiment?.id) return;

    this.loading.set(true);
    this.error.set(null);

    this.api
      .getExperimentRuns(this.experiment.id)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(
        (runs) => {
          const sorted = [...(runs ?? [])].sort(
            (a, b) => Date.parse(b.created_at) - Date.parse(a.created_at)
          );
          this.runs.set(sorted);
          this.loading.set(false);
        },
        (err) => {
          console.error(err);
          this.error.set("Couldn't load experiment runs.");
          this.loading.set(false);
        }
      );
  }

  async stopRun(id: string): Promise<void> {
    const popupInput: ConfirmPopupInput = {
      message: 'Do you wish to STOP this run?',
      acceptBtnMessage: 'Yes',
      declineBtnMessage: 'No',
    };

    const state = await firstValueFrom(
      this.dialog.open(UiConfirmComponent, { data: popupInput }).afterClosed()
    );

    if (state === ConfirmPopupResponse.Yes) {
      try {
        await firstValueFrom(this.api.stopExperimentRun(id));
        this.updateRuns();
      } catch (err) {
        console.error(err);
      }
    }
  }

  async deleteRun(id: string): Promise<void> {
    const popupInput: ConfirmPopupInput = {
      message: 'Do you wish to DELETE this run?',
      acceptBtnMessage: 'Yes',
      declineBtnMessage: 'No',
    };

    const state = await firstValueFrom(
      this.dialog.open(UiConfirmComponent, { data: popupInput }).afterClosed()
    );

    if (state === ConfirmPopupResponse.Yes) {
      try {
        await firstValueFrom(this.api.deleteExperimentRun(id));
        this.updateRuns();
      } catch (err) {
        console.error(err);
      }
    }
  }
}
