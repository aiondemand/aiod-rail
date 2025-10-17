import { Component, computed, effect, inject, signal } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet, NavigationEnd } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { BreakpointObserver } from '@angular/cdk/layout';
import { toSignal } from '@angular/core/rxjs-interop';
import { filter, map, startWith } from 'rxjs';
import { NavSection } from '../../../shared/nav/nav.types';
import { APP_NAV, ADMIN_NAV } from '../../../shared/nav/app.nav';

import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    MatSidenavModule,
    MatListModule,
    MatIconModule,
    MatDividerModule,
    MatButtonModule,
  ],
  styleUrls: ['./main-layout.scss'],
  templateUrl: './main-layout.html',
})
export class MainLayout {
  private router = inject(Router);
  private bp = inject(BreakpointObserver);
  private auth = inject(AuthService);

  /** URL as signal */
  url = toSignal(
    this.router.events.pipe(
      filter((e) => e instanceof NavigationEnd),
      startWith(null),
      map(() => this.router.url)
    ),
    { initialValue: this.router.url }
  );

  private wantsAdminFromUrl = computed(() => (this.url() || '').startsWith('/admin'));
  isAdmin = computed(() => this.auth.isLoggedIn() && this.auth.hasAdminRole());
  showAdminSection = computed(() => this.isAdmin() || this.wantsAdminFromUrl());

  sections = computed<NavSection[]>(() =>
    this.showAdminSection() ? [...APP_NAV, ...ADMIN_NAV] : APP_NAV
  );

  /** Desktop breakpoint */
  isNarrow = toSignal(this.bp.observe(['(max-width: 956px)']).pipe(map((r) => r.matches)), {
    initialValue: false,
  });
  mode = computed<'over' | 'side'>(() => (this.isNarrow() ? 'over' : 'side'));
  opened = computed<boolean>(() => !this.isNarrow());

  /** Mini (collapse) – only desktop */
  isCollapsed = signal(false);
  toggleCollapsed() {
    if (!this.isNarrow()) this.isCollapsed.update((v) => !v);
  }

  /** ===== Accordion ===== */
  private expandedIndex = signal<number | null>(null);

  private _autoOpen = effect(() => {
    const u = this.url() || '';
    const idx = this.indexForUrl(u);
    if (idx !== null) this.expandedIndex.set(idx);

    if (idx === null) {
      const first = this.sections().findIndex((s) => (s.items?.length ?? 0) > 0);
      this.expandedIndex.set(first >= 0 ? first : null);
    }
  });

  isCollapsible = (s: NavSection) => (s.collapsible ?? true) && (s.items?.length ?? 0) > 0;
  hasItems = (s: NavSection) => (s.items?.length ?? 0) > 0;
  isExpanded(i: number, _s: NavSection) {
    return this.expandedIndex() === i;
  }

  onSectionHeaderClick(i: number, s: NavSection, drawer: any) {
    this.expandedIndex.set(i);
    const target = s.items?.[0]?.slug ?? s.titleSlug ?? null;
    if (target) {
      this.router.navigateByUrl(target).then(() => {
        if (this.isNarrow()) drawer.close();
      });
    }
  }

  onItemClick(sectionIndex: number, drawer: any) {
    if (this.expandedIndex() !== sectionIndex) this.expandedIndex.set(sectionIndex);
    if (this.isNarrow()) drawer.close();
  }

  linkTo(slug?: string) {
    return slug || '/';
  }

  private indexForUrl(u: string): number | null {
    const secs = this.sections();
    for (let i = 0; i < secs.length; i++) {
      const s = secs[i];
      if (s.titleSlug && u.startsWith(s.titleSlug)) return i;
      if (s.items) {
        for (const it of s.items) {
          if (it.slug && u.startsWith(it.slug)) return i;
        }
      }
    }
    return null;
  }

  isExternalUrl(url?: string): boolean {
    return !!url && /^(https?:)?\/\//i.test(url);
  }

  go(url: string) {
    window.location.href = url;
  }
}
