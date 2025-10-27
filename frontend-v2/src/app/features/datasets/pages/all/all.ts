import { Component, OnInit, inject, signal, computed, DestroyRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import {
  map,
  switchMap,
  catchError,
  finalize,
  startWith,
  distinctUntilChanged,
} from 'rxjs/operators';
import { combineLatest, of } from 'rxjs';

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
  // ---- DI
  private api = inject(BackendApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  // ---- UI state (signals)
  items = signal<Dataset[]>([]);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  // Query/paging state (mirrors URL query params)
  pageSize = signal<number>(10);
  pageIndex = signal<number>(0);
  query = signal<string>('');
  enhanced = signal<boolean>(false);

  length = signal<number>(0); // total count

  // ---- Derived values for pagination UI
  offset = computed(() => this.pageIndex() * this.pageSize());
  canPrev = computed(() => this.pageIndex() > 0);
  canNext = computed(() => this.offset() + this.pageSize() < this.length());
  from = computed(() => (this.length() === 0 ? 0 : this.offset() + 1));
  to = computed(() => Math.min(this.offset() + this.pageSize(), this.length()));

  ngOnInit(): void {
    /**
     * Stream of URL query params -> normalized state object.
     * distinctUntilChanged prevents duplicate requests when params don't actually change.
     */
    this.route.queryParamMap
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        startWith(this.route.snapshot.queryParamMap), // run immediately on init
        map((params) => {
          const ps = this.toInt(params.get('pageSize'), this.pageSize());
          const pi = this.toInt(params.get('pageIndex'), this.pageIndex());
          const q = (params.get('q') ?? '').trim();
          const en = (params.get('enhanced') ?? 'false') === 'true';
          return { pageSize: ps, pageIndex: pi, q, enhanced: en };
        }),
        distinctUntilChanged((a, b) => JSON.stringify(a) === JSON.stringify(b)),

        /**
         * For every param set, update local signals for the UI,
         * then request list + count in parallel. `switchMap` cancels older requests
         * if params change while the backend is still responding.
         */
        switchMap(({ pageSize, pageIndex, q, enhanced }) => {
          // keep UI signals in sync with URL
          if (pageSize !== this.pageSize()) this.pageSize.set(pageSize);
          if (pageIndex !== this.pageIndex()) this.pageIndex.set(pageIndex);
          if (q !== this.query()) this.query.set(q);
          if (enhanced !== this.enhanced()) this.enhanced.set(enhanced);

          // prepare requests for the CURRENT param set
          const offset = pageIndex * pageSize;
          const list$ = this.api.getDatasets(q, { offset, limit: pageSize }, enhanced);
          const count$ = this.api.getDatasetsCount(q, enhanced);

          // set loading before the pair of requests
          this.loading.set(true);
          this.error.set(null);

          return combineLatest([list$, count$]).pipe(
            // Map to a single object to consume in one subscriber
            map(([list, count]) => ({
              list: list ?? [],
              count: count ?? 0,
            })),
            // On any error, surface message and fall back to empty results
            catchError((err) => {
              console.error(err);
              this.error.set(err?.error?.message || err?.message || 'Failed to load datasets.');
              return of({ list: [] as Dataset[], count: 0 });
            }),
            // Loading off regardless of success/failure
            finalize(() => this.loading.set(false))
          );
        })
      )
      .subscribe(({ list, count }) => {
        // Apply the latest (non-cancelled) results
        this.items.set(list);
        this.length.set(count);
      });
  }

  // ---- Toolbar handlers
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

  // Arrow buttons
  nextPage() {
    if (!this.canNext()) return;
    this.navigateWith({ pageIndex: this.pageIndex() + 1 });
  }
  prevPage() {
    if (!this.canPrev()) return;
    this.navigateWith({ pageIndex: this.pageIndex() - 1 });
  }

  // ---- Internal utils
  private toInt(v: string | null, fallback: number): number {
    if (v == null) return fallback;
    const n = Number(v);
    return Number.isFinite(n) && n >= 0 ? n : fallback;
  }

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
    this.navigateWith({});
  }
}
