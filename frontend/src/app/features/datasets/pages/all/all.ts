import { Component, OnInit, inject, signal, computed, DestroyRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import {
  map,
  switchMap,
  catchError,
  startWith,
  distinctUntilChanged,
  tap,
  retry,
} from 'rxjs/operators';
import { of, timer } from 'rxjs';

import { AssetCardComponent } from '../../../../shared/components/asset-card/asset-card';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';

import { Dataset } from '../../../../shared/models/dataset';
import { BackendApiService } from '../../../../shared/services/backend-api.service';

import { SearchToolbarComponent } from '../../../../shared/components/search-toolbar/search-toolbar';
import { UiLoadingComponent } from '../../../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';

type ParamState = {
  pageSize: number;
  pageIndex: number;
  q: string;
  enhanced: boolean;
};

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
  loading = signal<boolean>(true); // loading LISTU
  countLoading = signal<boolean>(true); // loading COUNTA
  error = signal<string | null>(null);

  // Query/paging state (mirrors URL query params)
  pageSize = signal<number>(10);
  pageIndex = signal<number>(0);
  query = signal<string>('');
  enhanced = signal<boolean>(false);

  length = signal<number | undefined>(undefined);

  // ---- Derived values for pagination UI
  offset = computed(() => this.pageIndex() * this.pageSize());
  canPrev = computed(() => this.pageIndex() > 0);
  canNext = computed(() => {
    const len = this.length();
    if (typeof len !== 'number') return false;
    return this.offset() + this.pageSize() < len;
  });
  from = computed(() => {
    const len = this.length();
    if (typeof len !== 'number') return 0;
    return len === 0 ? 0 : this.offset() + 1;
  });
  to = computed(() => {
    const len = this.length();
    if (typeof len !== 'number') return this.pageSize();
    return Math.min(this.offset() + this.pageSize(), len);
  });

  private activeListKey = signal<string>('');
  private activeCountKey = signal<string>('');

  private makeListKey(p: ParamState) {
    return `q=${p.q}|enh=${p.enhanced ? 1 : 0}|ps=${p.pageSize}|pi=${p.pageIndex}`;
  }
  private makeCountKey(p: Pick<ParamState, 'q' | 'enhanced'>) {
    return `q=${p.q}|enh=${p.enhanced ? 1 : 0}`;
  }

  ngOnInit(): void {
    const params$ = this.route.queryParamMap.pipe(
      takeUntilDestroyed(this.destroyRef),
      startWith(this.route.snapshot.queryParamMap),
      map((params) => {
        const ps = this.toInt(params.get('pageSize'), this.pageSize());
        const pi = this.toInt(params.get('pageIndex'), this.pageIndex());
        const q = (params.get('q') ?? '').trim();
        const en = (params.get('enhanced') ?? 'false') === 'true';
        return { pageSize: ps, pageIndex: pi, q, enhanced: en } as ParamState;
      }),
      distinctUntilChanged((a, b) => JSON.stringify(a) === JSON.stringify(b)),
      tap((p) => {
        // sync UI
        if (p.pageSize !== this.pageSize()) this.pageSize.set(p.pageSize);
        if (p.pageIndex !== this.pageIndex()) this.pageIndex.set(p.pageIndex);
        if (p.q !== this.query()) this.query.set(p.q);
        if (p.enhanced !== this.enhanced()) this.enhanced.set(p.enhanced);

        // set list key
        this.activeListKey.set(this.makeListKey(p));
      })
    );

    // 2) LIST pipeline
    params$
      .pipe(
        switchMap((p) => {
          const offset = p.pageIndex * p.pageSize;

          this.error.set(null);
          this.loading.set(true);

          return this.api.getDatasets(p.q, { offset, limit: p.pageSize }, p.enhanced).pipe(
            map((list) => ({ list: list ?? [], key: this.makeListKey(p) })),
            catchError((err) => {
              console.error(err);
              this.error.set(err?.error?.message || err?.message || 'Failed to load datasets.');
              return of({ list: [] as Dataset[], key: this.makeListKey(p) });
            }),
            tap(() => this.loading.set(false))
          );
        })
      )
      .subscribe(({ list, key }) => {
        if (key !== this.activeListKey()) return;
        this.items.set(list);
      });

    // 3) COUNT pipeline
    const countParams$ = params$.pipe(
      map((p) => ({ q: p.q, enhanced: p.enhanced })),
      distinctUntilChanged((a, b) => a.q === b.q && a.enhanced === b.enhanced),
      tap((p) => {
        // reset count state
        this.activeCountKey.set(this.makeCountKey(p));
        this.countLoading.set(true);
        this.length.set(undefined);
      })
    );

    countParams$
      .pipe(
        switchMap((p) => {
          const key = this.makeCountKey(p);
          return this.api.getDatasetsCount(p.q, p.enhanced).pipe(
            retry({
              delay: (error, retryIndex) => {
                const ms = Math.min(30000, 1000 * Math.pow(2, retryIndex));
                return timer(ms);
              },
            }),
            map((count) => ({ count, key })),
            catchError(() => of({ count: undefined as number | undefined, key }))
          );
        })
      )
      .subscribe(({ count, key }) => {
        if (key !== this.activeCountKey()) return;

        if (typeof count === 'number' && Number.isFinite(count) && count >= 0) {
          this.length.set(count);
          this.countLoading.set(false);
        } else {
          // count neznámy -> nechaj spinner
          this.countLoading.set(true);
        }
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
