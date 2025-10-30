import { Component, OnInit, inject, signal, computed, DestroyRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { AssetCardComponent } from '../../../../shared/components/asset-card/asset-card';
import { SearchToolbarComponent } from '../../../../shared/components/search-toolbar/search-toolbar';
import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { Dataset } from '../../../../shared/models/dataset';

@Component({
  selector: 'app-my-datasets',
  standalone: true,
  imports: [
    CommonModule,
    AssetCardComponent,
    SearchToolbarComponent,
    UiLoadingComponent,
    UiErrorComponent,
  ],
  templateUrl: './my-datasets.html',
  styleUrls: ['./my-datasets.scss'],
})
export class MyDatasetsComponent implements OnInit {
  private api = inject(BackendApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  // UI state
  items = signal<Dataset[]>([]);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  // paging (sync with URL)
  pageSize = signal<number>(10);
  pageIndex = signal<number>(0);
  length = signal<number>(0); // total count

  // computed helpers
  offset = computed(() => this.pageIndex() * this.pageSize());
  from = computed(() => (this.length() === 0 ? 0 : this.offset() + 1));
  to = computed(() => Math.min(this.offset() + this.pageSize(), this.length()));

  ngOnInit(): void {
    this.route.queryParamMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((params) => {
      const ps = this.toInt(params.get('pageSize'), this.pageSize());
      const pi = this.toInt(params.get('pageIndex'), this.pageIndex());

      if (ps !== this.pageSize()) this.pageSize.set(ps);
      if (pi !== this.pageIndex()) this.pageIndex.set(pi);

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

    // data
    this.api
      .getMyDatasets('', { offset: this.offset(), limit: this.pageSize() })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (ds) => {
          this.items.set(ds ?? []);
          this.loading.set(false);
        },
        error: (err) => {
          console.error(err);
          this.error.set(err?.error?.message || err?.message || 'Failed to load datasets.');
          this.loading.set(false);
        },
      });

    // count
    this.api
      .getMyDatasetsCount()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (cnt) => this.length.set(cnt ?? 0),
        error: (err) => console.warn('Count failed:', err),
      });
  }

  // toolbar handlers
  changePageSize(ps: number) {
    this.navigateWith({ pageSize: ps, pageIndex: 0 });
  }

  onPageIndexChange(i: number) {
    this.navigateWith({ pageIndex: i });
  }

  // internals
  private navigateWith(patch: Partial<{ pageSize: number; pageIndex: number }>) {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        pageSize: patch.pageSize ?? this.pageSize(),
        pageIndex: patch.pageIndex ?? this.pageIndex(),
      },
      queryParamsHandling: 'merge',
    });
  }

  onRetryError() {
    this.load();
  }
}
