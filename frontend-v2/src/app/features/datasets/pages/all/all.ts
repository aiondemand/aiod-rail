import { Component, OnInit, inject, signal, computed, DestroyRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { tap } from 'rxjs/operators';

import { AssetCardComponent } from '../../../../shared/components/asset-card/asset-card';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';

import { Dataset } from '../../../../shared/models/dataset';
import { BackendApiService } from '../../../../shared/services/backend-api.service';

import { SearchToolbarComponent } from '../../../../shared/components/search-toolbar/search-toolbar';

import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';

@Component({
  selector: 'app-datasets-all',
  standalone: true,
  imports: [
    CommonModule,
    AssetCardComponent,
    MatSelectModule,
    MatIconModule,
    SearchToolbarComponent,
    UiLoadingComponent,
    UiErrorComponent,
  ],
  templateUrl: './all.html',
  styleUrls: ['./all.scss'],
})
export class DatasetsAllComponent implements OnInit {
  private api = inject(BackendApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  // UI state
  items = signal<Dataset[]>([]);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  // query/paging (sync with URL)
  pageSize = signal<number>(10);
  pageIndex = signal<number>(0);
  query = signal<string>('');
  enhanced = signal<boolean>(false);

  length = signal<number>(0); // total count

  // computed
  offset = computed(() => this.pageIndex() * this.pageSize());
  canPrev = computed(() => this.pageIndex() > 0);
  canNext = computed(() => this.offset() + this.pageSize() < this.length());

  //  UI
  from = computed(() => (this.length() === 0 ? 0 : this.offset() + 1));
  to = computed(() => Math.min(this.offset() + this.pageSize(), this.length()));

  ngOnInit(): void {
    this.route.queryParamMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((params) => {
      const ps = this.toInt(params.get('pageSize'), this.pageSize());
      const pi = this.toInt(params.get('pageIndex'), this.pageIndex());
      const q = params.get('q') ?? '';
      const en = (params.get('enhanced') ?? 'false') === 'true';

      if (ps !== this.pageSize()) this.pageSize.set(ps);
      if (pi !== this.pageIndex()) this.pageIndex.set(pi);
      if (q !== this.query()) this.query.set(q);
      if (en !== this.enhanced()) this.enhanced.set(en);

      this.load();
    });
  }

  private toInt(v: string | null, fallback: number): number {
    if (v == null) return fallback;
    const n = Number(v);
    return Number.isFinite(n) && n >= 0 ? n : fallback;
  }

  private load() {
    this.loading.set(true);
    this.error.set(null);

    this.api
      .getDatasets(this.query(), { offset: this.offset(), limit: this.pageSize() }, this.enhanced())
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (ds) => {
          this.items.set(ds ?? []);
          this.loading.set(false);
        },
        error: (err) => {
          console.error(err);
          this.error.set(err?.error?.message || err?.message || 'failed to load datasets.');
          this.loading.set(false);
        },
      });

    this.api
      .getDatasetsCount(this.query(), this.enhanced())
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (cnt) => this.length.set(cnt ?? 0),
        error: (err) => console.warn('Count failed:', err),
      });
  }

  // === Handlers from toolbar ===
  onSearch(v: string) {
    const q = v?.trim() ?? '';
    this.navigateWith({ q, pageIndex: 0 });
  }

  toggleEnhanced(on: boolean) {
    this.navigateWith({ enhanced: on, pageIndex: 0 });
  }

  changePageSize(ps: number) {
    this.navigateWith({ pageSize: ps, pageIndex: 0 });
  }

  onPageIndexChange(i: number) {
    this.navigateWith({ pageIndex: i });
  }

  // variable buttons
  nextPage() {
    if (!this.canNext()) return;
    this.navigateWith({ pageIndex: this.pageIndex() + 1 });
  }
  prevPage() {
    if (!this.canPrev()) return;
    this.navigateWith({ pageIndex: this.pageIndex() - 1 });
  }

  // === Intern ===
  private navigateWith(
    patch: Partial<{ q: string; pageSize: number; pageIndex: number; enhanced: boolean }>
  ) {
    const enhancedFlag = patch.enhanced ?? this.enhanced() ? 'true' : 'false';
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        q: patch.q ?? this.query(),
        pageSize: patch.pageSize ?? this.pageSize(),
        pageIndex: patch.pageIndex ?? this.pageIndex(),
        enhanced: enhancedFlag,
      },
      queryParamsHandling: 'merge',
    });
  }

  onRetryError() {
    this.load();
  }
}
