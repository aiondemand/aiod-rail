import { Component, computed, DestroyRef, effect, input, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { interval, switchMap, map } from 'rxjs';

import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTreeModule } from '@angular/material/tree';
import { MatTooltipModule } from '@angular/material/tooltip';
import { NestedTreeControl } from '@angular/cdk/tree';
import { ScrollingModule } from '@angular/cdk/scrolling';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { SnackBarService } from '../../../../shared/services/snack-bar.service';
import { MatDialog } from '@angular/material/dialog';
import { UiConfirmComponent } from '../../../../shared/components/ui-confirm/ui-confirm';
import { ConfirmPopupInput, ConfirmPopupResponse } from '../../../../shared/models/popup';
import { Experiment } from '../../../../shared/models/experiment';
import { ExperimentRunDetails } from '../../../../shared/models/experiment-run';
import { FileDetail } from '../../../../shared/models/file-detail';
import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';
import { UiButton } from '../../../../shared/components/ui-button/ui-button';

type RunState = 'CREATED' | 'PREPROCESSING' | 'RUNNING' | 'POSTPROCESSING' | 'FINISHED' | 'CRASHED';

interface FileNode {
  name: string;
  filepath: string;
  last_modified?: string;
  size?: number;
  children?: FileNode[];
}

@Component({
  selector: 'app-experiment-run-detail',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatButtonModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    MatTreeModule,
    MatTooltipModule,
    ScrollingModule,
    UiLoadingComponent,
    UiErrorComponent,
    UiButton,
  ],
  templateUrl: './experiment-run-detail.html',
  styleUrls: ['./experiment-run-detail.scss'],
})
export class ExperimentRunDetailComponent {
  // ---- DI
  private backend = inject(BackendApiService);
  private snackBar = inject(SnackBarService);
  private dialog = inject(MatDialog);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private destroyRef = inject(DestroyRef);

  // ---- Input (alebo z URL)
  runId = input<string>('');
  private routeRunId = toSignal(this.route.paramMap.pipe(map((pm) => pm.get('runId') ?? '')), {
    initialValue: '',
  });
  private effectiveRunId = computed(() => this.runId() || this.routeRunId());

  // ---- State
  experiment = signal<Experiment | null>(null);
  run = signal<ExperimentRunDetails | null>(null);
  logs = signal<string>('');
  downloading = signal<Set<string>>(new Set());

  // loading & error  <ui-loading> a <ui-error>
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  // trigger for manual „retry“
  private refreshKey = signal(0);
  reload = () => {
    this.error.set(null);
    this.loading.set(true);
    this.refreshKey.update((v) => v + 1);
  };

  // --- Logs & virtual scroll
  logLines = computed(() => (this.logs() ?? '').split('\n'));
  private static readonly VSCROLL_THRESHOLD = 800;
  useVirtualScroll = computed(
    () => this.logLines().length > ExperimentRunDetailComponent.VSCROLL_THRESHOLD
  );
  trackByIndex = (i: number) => i;

  // --- Nested tree
  private fileTree = signal<FileNode[]>([]);
  dataSource = computed(() => this.fileTree());
  treeControl = new NestedTreeControl<FileNode>((node) => node.children ?? []);
  hasChild = (_: number, node: FileNode) => !!node.children?.length;

  isMine = computed(() => this.run()?.is_mine ?? false);
  isArchived = computed(() => this.run()?.is_archived ?? false);
  state = computed<RunState | null>(() => (this.run()?.state as RunState) ?? null);
  isRunningLike = computed(() =>
    ['CREATED', 'PREPROCESSING', 'RUNNING', 'POSTPROCESSING'].includes(this.state() ?? '')
  );

  constructor() {
    effect(() => {
      const id = this.effectiveRunId();
      const _refresh = this.refreshKey();
      if (!id) return;

      this.loading.set(true);
      this.error.set(null);

      this.backend
        .getExperimentRun(id)
        .pipe(takeUntilDestroyed(this.destroyRef))
        .subscribe({
          next: (r) => {
            this.run.set(r);
            this.logs.set(extractLogs(r?.logs));

            // get experiment
            this.backend
              .getExperiment(r.experiment_id)
              .pipe(takeUntilDestroyed(this.destroyRef))
              .subscribe({
                next: (e) => {
                  this.experiment.set(e);
                  this.loading.set(false);
                },
                error: (err2) => {
                  console.error(err2);
                  this.error.set(
                    err2?.error?.message || err2?.message || 'Failed to load experiment.'
                  );
                  this.loading.set(false);
                },
              });

            // load files
            if (r.state === 'FINISHED' || r.state === 'CRASHED') this.loadFiles(r.id);
          },
          error: (err) => {
            this.snackBar.showError(`Couldn't load experiment run: ${err.message}`);
            console.error(err);
            this.error.set(err?.error?.message || err?.message || 'Failed to load experiment run.');
            this.loading.set(false);
          },
        });
    });

    effect((onCleanup) => {
      if (this.error()) return;
      if (!this.isRunningLike()) return;

      const id = this.effectiveRunId();
      if (!id) return;

      const sub = interval(5000)
        .pipe(switchMap(() => this.backend.getExperimentRun(id)))
        .subscribe({
          next: (r) => {
            this.run.set(r);
            this.logs.set(extractLogs(r?.logs));
            if (r.state === 'FINISHED' || r.state === 'CRASHED') {
              this.loadFiles(r.id);
              sub.unsubscribe();
            }
          },
          error: (err) => this.snackBar.showError(`Polling failed: ${err.message}`),
        });

      onCleanup(() => sub.unsubscribe());
    });
  }

  // ---- Actions
  stopRun(): void {
    const r = this.run();
    const e = this.experiment();
    if (!r || !e) return;

    const popup: ConfirmPopupInput = {
      message: 'Do you wish to STOP this run?',
      acceptBtnMessage: 'Yes',
      declineBtnMessage: 'No',
    };

    this.dialog
      .open(UiConfirmComponent, { maxWidth: '450px', width: '100%', autoFocus: false, data: popup })
      .afterClosed()
      .subscribe((res: ConfirmPopupResponse) => {
        if (res === ConfirmPopupResponse.Yes) {
          this.backend
            .stopExperimentRun(r.id)
            .pipe(takeUntilDestroyed(this.destroyRef))
            .subscribe({
              next: () => this.router.navigate(['/experiments', e.id]),
              error: (err) => console.error(err),
            });
        }
      });
  }

  deleteRun(): void {
    const r = this.run();
    const e = this.experiment();
    if (!r || !e) return;

    const popup: ConfirmPopupInput = {
      message: 'Do you wish to DELETE this run?',
      acceptBtnMessage: 'Yes',
      declineBtnMessage: 'No',
    };

    this.dialog
      .open(UiConfirmComponent, { maxWidth: '450px', width: '100%', autoFocus: false, data: popup })
      .afterClosed()
      .subscribe((res: ConfirmPopupResponse) => {
        if (res === ConfirmPopupResponse.Yes) {
          this.backend
            .deleteExperimentRun(r.id)
            .pipe(takeUntilDestroyed(this.destroyRef))
            .subscribe({
              next: () => this.router.navigate(['/experiments', e.id]),
              error: (err) => console.error(err),
            });
        }
      });
  }

  downloadFile(event: Event, filepath: string) {
    event.stopPropagation();

    const set = new Set(this.downloading());
    set.add(filepath);
    this.downloading.set(set);
    const runId = this.run()?.id;
    if (!runId) return;

    this.backend
      .downloadFileFromExperimentRun(runId, filepath)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          const blobObj = new Blob([response.body], { type: response.body.type });
          const url = window.URL.createObjectURL(blobObj);
          const link = document.createElement('a');

          const filename = parseFilename(response.headers.get('content-disposition') ?? '');
          link.href = url;
          link.download = filename;
          link.style.display = 'none';
          document.body.appendChild(link);
          link.click();

          window.URL.revokeObjectURL(url);
          document.body.removeChild(link);

          const after = new Set(this.downloading());
          after.delete(filepath);
          this.downloading.set(after);
        },
        error: () => {
          const after = new Set(this.downloading());
          after.delete(filepath);
          this.downloading.set(after);
        },
      });
  }

  // ---- Helpers
  formatFileSize(size?: number): string {
    if (size == null) return '';
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let i = 0;
    let s = size;
    while (s >= 1024 && i < units.length - 1) {
      s /= 1024;
      i++;
    }
    return `${Math.round(s * 100) / 100} ${units[i]}`;
  }

  private loadFiles(runId: string) {
    this.backend
      .listFilesFromExperimentRun(runId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (files) => this.fileTree.set(buildTree(files)),
        error: (err) => console.error(err),
      });
  }
}

// ---------- pure helpers ----------
function extractLogs(raw?: string | null): string {
  if (!raw) return '';
  try {
    const parsed = JSON.parse(raw);
    const jobLogs = parsed?.['job_logs'];
    const firstKey = jobLogs ? Object.keys(jobLogs)[0] : null;
    return firstKey ? jobLogs[firstKey]?.['logs'] ?? '' : '';
  } catch {
    return '';
  }
}

function parseFilename(contentDisposition: string): string {
  const match = /filename\*=UTF-8''([^;]+)|filename="?([^";]+)"?/i.exec(contentDisposition);
  return decodeURIComponent(match?.[1] ?? match?.[2] ?? 'download');
}

function buildTree(files: FileDetail[]): FileNode[] {
  const root: FileNode[] = [];
  const ensureDir = (arr: FileNode[], name: string, path: string): FileNode => {
    const existing = arr.find((n) => n.filepath === path && n.children);
    if (existing) return existing;
    const node: FileNode = {
      name: name.endsWith('/') ? name : name + '/',
      filepath: path,
      children: [],
    };
    insertSorted(arr, node);
    return node;
  };

  for (const f of files) {
    const parts = f.filepath.split('/');
    let cursor = root;

    parts.forEach((seg, idx) => {
      const currPath = parts.slice(0, idx + 1).join('/');
      const isLeaf = idx === parts.length - 1;

      if (isLeaf) {
        const leaf: FileNode = {
          name: seg,
          filepath: f.filepath,
          last_modified: f.last_modified,
          size: f.size,
        };
        insertSorted(cursor, leaf);
      } else {
        const dir = ensureDir(cursor, seg, currPath);
        cursor = dir.children!;
      }
    });
  }
  return root;
}

function insertSorted(target: FileNode[], node: FileNode) {
  const key = (n: FileNode) => (n.children ? '0' : '1') + n.name.toLowerCase(); // dirs first
  target.push(node);
  target.sort((a, b) => key(a).localeCompare(key(b)));
}
