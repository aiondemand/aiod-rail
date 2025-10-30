import { Component, OnInit, DestroyRef, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

import { BackendApiService } from '../../../../shared/services/backend-api.service';
import { SearchToolbarComponent } from '../../../../shared/components/search-toolbar/search-toolbar';
import { UiErrorComponent } from '../../../../shared/components/ui-error/ui-error';
import { AssetCardComponent } from '../../../../shared/components/asset-card/asset-card';

import { ExperimentTemplate } from '../../../../shared/models/experiment-template';

@Component({
  selector: 'app-my-templates',
  standalone: true,
  imports: [CommonModule, SearchToolbarComponent, UiErrorComponent, AssetCardComponent],

  templateUrl: '../templates/templates.html',
  styleUrls: ['../templates/templates.scss'],
})
export class MyTemplatesPage implements OnInit {
  private api = inject(BackendApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  items = signal<ExperimentTemplate[]>([]);
  loading = signal<boolean>(true);
  error = signal<string | null>(null);

  pageSize = signal<number>(10);
  pageIndex = signal<number>(0);
  query = signal<string>('');
  length = signal<number>(0);

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

  private load() {
    this.loading.set(true);
    this.error.set(null);

    this.api
      .getExperimentTemplates(
        this.query(),
        { offset: this.offset(), limit: this.pageSize() },
        { mine: true }
      )
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (xs) => {
          this.items.set(xs ?? []);
          this.loading.set(false);
        },
        error: (err) => {
          console.error(err);
          this.error.set(err?.error?.message || err?.message || 'Could not load templates.');
          this.loading.set(false);
        },
      });

    this.api
      .getExperimentTemplatesCount(this.query(), { mine: true })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (cnt) => this.length.set(cnt ?? 0),
        error: (err) => console.warn('Count failed:', err),
      });
  }

  // handlers
  onSearch(v: string) {
    this.navigateWith({ q: v?.trim() ?? '', pageIndex: 0 });
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

  // utils
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

  titleOf(t: ExperimentTemplate) {
    return (t as any).name ?? (t as any).title ?? '';
  }
  descOf(t: ExperimentTemplate) {
    return (t as any).description ?? (t as any).summary ?? '';
  }
  dateOf(t: ExperimentTemplate) {
    return (t as any).created_at ?? (t as any).createdAt ?? (t as any).date ?? undefined;
  }
  platformOf(t: ExperimentTemplate) {
    return (t as any).platform ?? (t as any).docker_image ?? '';
  }
  visibilityOf(t: ExperimentTemplate): 'public' | 'private' | 'unlisted' | '' {
    if ((t as any)?.is_public === true) return 'public';
    if ((t as any)?.is_public === false) return 'private';
    const v = (t as any).visibility ?? '';
    return v === 'public' || v === 'private' || v === 'unlisted' ? v : '';
  }
  linkOf(t: ExperimentTemplate): any[] {
    return ['/templates', (t as any).id ?? (t as any).identifier ?? ''];
  }
  trackT(t: ExperimentTemplate): string {
    return (t as any).id ?? (t as any).identifier ?? JSON.stringify(t);
  }

  approvedOf(t: any): boolean | null {
    return t?.is_approved ?? t?.approved ?? null;
  }
  archivedOf(t: any): boolean | null {
    return t?.is_archived ?? t?.archived ?? null;
  }
  stateOf(t: any): string | null {
    return t?.state ?? t?.status ?? null;
  }
}
