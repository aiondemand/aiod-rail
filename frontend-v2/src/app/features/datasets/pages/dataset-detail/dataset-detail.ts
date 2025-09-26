import {
  Component,
  DestroyRef,
  Input,
  ViewChild,
  ElementRef,
  inject,
  signal,
  computed,
  effect,
  Injector,
  OnInit,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDividerModule } from '@angular/material/divider';
import { MarkdownModule } from 'ngx-markdown';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { UiButton } from '../../../../shared/components/ui-button/ui-button';
import { Dataset } from '../../../../shared/models/dataset';
import { BackendApiService } from '../../../../shared/services/backend-api.service';

@Component({
  selector: 'app-dataset-detail',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatChipsModule,
    MatTooltipModule,
    MatDividerModule,
    MarkdownModule,
    UiButton,
    MatProgressSpinnerModule,
  ],
  templateUrl: './dataset-detail.html',
  styleUrls: ['./dataset-detail.scss'],
})
export class DatasetDetailComponent implements OnInit {
  private api = inject(BackendApiService);
  private route = inject(ActivatedRoute);
  private destroyRef = inject(DestroyRef);
  private injector = inject(Injector);

  @ViewChild('shortDescription') shortDescEl?: ElementRef<HTMLElement>;

  // state
  dataset = signal<Dataset | null>(null);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  showFull = signal<boolean>(false);
  canExpand = signal<boolean>(false);

  // input / route id
  private _id = signal<string | null>(null);
  @Input() set id(v: string | null) {
    if (v) this._id.set(v);
  }

  // computed
  title = computed(() => this.dataset()?.name ?? 'Dataset');
  version = computed(() => this.dataset()?.version ?? '');
  keywords = computed(() => this.dataset()?.keyword ?? []);
  platform = computed(() => this.dataset()?.platform ?? '');
  sameAs = computed(() => this.dataset()?.same_as ?? '');
  license = computed(() => (this.dataset()?.license || 'Unknown').toUpperCase());
  identifier = computed(() => this.dataset()?.identifier || 'Unknown');
  datePublished = computed(() => this.dataset()?.date_published || null);
  descriptionMd = computed(() => this.dataset()?.description?.plain ?? '');

  // ===== Effects  =====

  private readonly fetchEffect = effect(
    () => {
      const id = this._id();
      if (!id) return;
      this.fetch(id);
    },
    { injector: this.injector }
  );

  private readonly clampEffect = effect(
    () => {
      void this.descriptionMd();
      void this.showFull();

      queueMicrotask(() => {
        const el = this.shortDescEl?.nativeElement;
        if (!el) {
          this.canExpand.set(false);
          return;
        }
        const can = this.showFull() || el.scrollHeight - 2 > el.clientHeight;
        this.canExpand.set(can);
      });
    },
    { injector: this.injector }
  );

  ngOnInit(): void {
    this.route.paramMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((pm) => {
      const rid = pm.get('id');
      if (rid) this._id.set(rid);
    });
  }

  private fetch(id: string) {
    this.loading.set(true);
    this.error.set(null);

    this.api
      .getDataset(id)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (ds) => {
          this.dataset.set(ds ?? null);
          this.loading.set(false);
          this.showFull.set(false);
        },
        error: (err) => {
          console.error(err);
          this.error.set(err?.error?.message || err?.message || 'Dataset filed to load');
          this.loading.set(false);
        },
      });
  }

  toggleDescription(full: boolean) {
    this.showFull.set(full);
  }
}
