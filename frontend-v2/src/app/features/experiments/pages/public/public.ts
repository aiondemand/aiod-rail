import { Component, OnInit, DestroyRef, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { SearchToolbarComponent } from '../../../../shared/components/search-toolbar/search-toolbar';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';
import { AssetCardComponent } from '../../../../shared/components/asset-card/asset-card';

import { Experiment } from '../../../../shared/models/experiment';

@Component({
  selector: 'app-public',
  standalone: true,
  imports: [CommonModule, SearchToolbarComponent, UiErrorComponent, AssetCardComponent],
  templateUrl: './public.html',
  styleUrls: ['./public.scss'],
})
export class PublicPage implements OnInit {
  private api = inject(BackendApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  // ---- state (signals)
  items = signal<Experiment[]>([]);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  // ---- paging / query (URL-sync)
  pageSize = signal<number>(10);
  pageIndex = signal<number>(0);
  query = signal<string>('');
  length = signal<number>(0);

  // ---- derived
  offset = computed(() => this.pageIndex() * this.pageSize());

  ngOnInit(): void {
    this.route.queryParamMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((params) => {
      const ps = this.toInt(params.get('pageSize'), this.pageSize());
      const pi = this.toInt(params.get('pageIndex'), this.pageIndex());
      const q = params.get('q') ?? '';

      if (ps !== this.pageSize()) this.pageSize.set(ps);
      if (pi !== this.pageIndex()) this.pageIndex.set(pi);
      if (q !== this.query()) this.query.set(q);

      this.load();
    });
  }

  // ---- data loaders
  private load() {
    this.loading.set(true);
    this.error.set(null);

    this.api
      .getExperiments(
        this.query(),
        {
          offset: this.offset(),
          limit: this.pageSize(),
        },
        {
          public: true,
          archived: false,
        }
      )
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (xs: Experiment[]) => {
          this.items.set(xs ?? []);
          this.loading.set(false);
        },
        error: (err: any) => {
          console.error(err);
          this.error.set(
            err?.error?.message ?? err?.message ?? 'Could not load public experiments.'
          );
          this.loading.set(false);
        },
      });

    this.api
      .getExperimentsCount(this.query(), {
        public: true,
        archived: false,
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (cnt: number) => this.length.set(cnt ?? 0),
        error: (err: any) => {
          console.warn('Count failed:', err);
        },
      });
  }

  // ---- handlers (public API template)
  onSearch(v: string) {
    const q = v?.trim() ?? '';
    this.navigateWith({ q, pageIndex: 0 });
  }
  onPageSize(ps: number) {
    this.navigateWith({ pageSize: ps, pageIndex: 0 });
  }
  onPageIndex(i: number) {
    this.navigateWith({ pageIndex: i });
  }
  onRetryError() {
    this.load();
  }
  onDismissError() {
    this.error.set(null);
  }

  // ---- utils
  private navigateWith(patch: Partial<{ q: string; pageSize: number; pageIndex: number }>) {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        q: patch.q ?? this.query(),
        pageSize: patch.pageSize ?? this.pageSize(),
        pageIndex: patch.pageIndex ?? this.pageIndex(),
      },
      queryParamsHandling: 'merge',
    });
  }
  private toInt(v: string | null, fallback: number): number {
    if (v == null) return fallback;
    const n = Number(v);
    return Number.isFinite(n) && n >= 0 ? n : fallback;
  }

  titleOf(exp: Experiment): string {
    return (exp as any).name ?? (exp as any).title ?? '';
  }
  descOf(exp: Experiment): string {
    return (exp as any).description ?? (exp as any).summary ?? '';
  }
  dateOf(exp: Experiment): string | number | Date | undefined {
    return (exp as any).created_at ?? (exp as any).createdAt ?? (exp as any).date ?? undefined;
  }
  platformOf(exp: Experiment): string {
    return (exp as any).platform ?? '';
  }
  visibilityOf(exp: Experiment): 'public' | 'private' | 'unlisted' | '' {
    // boolean flag
    if ((exp as any)?.is_public === true) return 'public';
    if ((exp as any)?.is_public === false) return 'private';

    // if as response from api is 'visibility'
    const v = (exp as any).visibility ?? '';
    return v === 'public' || v === 'private' || v === 'unlisted' ? v : '';
  }
  linkOf(exp: Experiment): any[] {
    return ['/experiments', (exp as any).id ?? (exp as any).identifier ?? ''];
  }
  trackExp(exp: Experiment): string {
    return (exp as any).id ?? (exp as any).identifier ?? JSON.stringify(exp);
  }
}
