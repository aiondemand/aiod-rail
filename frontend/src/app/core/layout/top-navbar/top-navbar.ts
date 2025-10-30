import { CommonModule, isPlatformBrowser } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  HostListener,
  OnDestroy,
  OnInit,
  Renderer2,
  inject,
  signal,
} from '@angular/core';
import { PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ThemeSwitch } from '../../../shared/components/theme-switch/theme-switch';
import { LoginLogoutComponent } from '../../../shared/components/login-logout/login-logout';
import { UiButton } from '../../../shared/components/ui-button/ui-button';
import { MatIconModule } from '@angular/material/icon';

type NavItem = {
  id: number;
  title: string;
  url?: string;
  description?: string;
  parent: string | number;
  isHighlighted?: boolean; // používame pre žltú šípku + špec. hover
  children?: NavItem[];
  open?: boolean;
};

const EXTERNAL = {
  GET_STARTED: 'https://aiod.eu/get-started',
  MY_LIBRARY: 'https://mylibrary.aiod.eu',
  TECH_SUPPORT: 'https://aiod.eu/technical-support/',
};

@Component({
  selector: 'app-top-navbar',
  standalone: true,
  imports: [CommonModule, ThemeSwitch, LoginLogoutComponent, UiButton, MatIconModule],
  templateUrl: './top-navbar.html',
  styleUrls: ['./top-navbar.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TopNavbar implements OnInit, OnDestroy {
  private http = inject(HttpClient);
  private renderer = inject(Renderer2);
  private platformId = inject(PLATFORM_ID);

  protected external = EXTERNAL;
  protected menu = signal<NavItem[]>([]);
  protected mobileOpened = signal(false);
  protected isDesktop = signal<boolean>(true);

  private get isBrowser() {
    return isPlatformBrowser(this.platformId);
  }

  ngOnInit(): void {
    if (this.isBrowser) {
      this.isDesktop.set(window.innerWidth >= 992);

      const saved = localStorage.getItem('theme') as 'light' | 'dark' | null;
      if (saved) this.toggleThemeTo(saved);

      const media = window.matchMedia?.('(prefers-color-scheme: dark)');
      media?.addEventListener?.('change', (e) => this.toggleThemeTo(e.matches ? 'dark' : 'light'));
    }

    this.fetchNavigation();
  }

  ngOnDestroy(): void {}

  private fetchNavigation(): void {
    this.http.get<NavItem[]>('https://aiod.eu/wp-json/aiod/v1/navigation').subscribe({
      next: (items) => this.menu.set(this.normalize(items ?? [])),
      error: () => this.menu.set([]),
    });
  }

  private normalize(items: NavItem[]): NavItem[] {
    const attach = (it: NavItem): NavItem => ({
      ...it,
      id: Number(it.id),
      children: (it.children ?? []).map(attach),
      open: false,
    });
    return items.map(attach);
  }

  // ===== theme =====
  protected toggleTheme(): void {
    if (!this.isBrowser) return;
    const html = document.documentElement;
    const next =
      (html.getAttribute('data-theme') as 'light' | 'dark') === 'light' ? 'dark' : 'light';
    this.toggleThemeTo(next);
  }
  protected toggleThemeTo(theme: 'light' | 'dark') {
    if (!this.isBrowser) return;
    this.renderer.setAttribute(document.documentElement, 'data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  // ===== responsive =====
  @HostListener('window:resize')
  onResize() {
    if (!this.isBrowser) return;
    const desktop = window.innerWidth >= 992;
    if (desktop !== this.isDesktop()) {
      this.isDesktop.set(desktop);
      if (desktop) this.mobileOpened.set(false);
    }
  }

  protected openMobileMenu() {
    if (!this.isBrowser) return;
    this.mobileOpened.set(!this.mobileOpened());
  }

  protected toggleSubmenuMobile(item: NavItem, ev: Event) {
    if (this.isDesktop()) return;
    if (item.children && item.children.length) {
      ev.preventDefault();
      item.open = !item.open;
    }
  }

  protected targetFor(url?: string) {
    if (!url) return null;
    return /^https?:\/\//i.test(url) ? '_blank' : null;
  }

  // ===== open external for ui-button =====
  protected openExternal(url: string) {
    if (!this.isBrowser) return;
    window.open(url, '_self');
  }

  protected isTools(title?: string) {
    return (title || '').trim().toLowerCase() === 'tools';
  }
}
