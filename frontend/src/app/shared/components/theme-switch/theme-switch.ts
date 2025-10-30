import { Component, effect, signal, Input, computed } from '@angular/core';

type Size = 'sm' | 'md' | 'lg';

@Component({
  selector: 'theme-switch',
  standalone: true,
  templateUrl: './theme-switch.html',
  styleUrls: ['./theme-switch.scss'],
})
export class ThemeSwitch {
  @Input() size: Size = 'md';

  mode = signal<'light' | 'dark'>(this.getInitial());
  readonly isDark = computed(() => this.mode() === 'dark');

  constructor() {
    effect(() => this.apply(this.mode()));
  }

  toggle() {
    const next = this.isDark() ? 'light' : 'dark';
    this.mode.set(next);
    if (this.isBrowser()) localStorage.setItem('theme', next);
  }

  private getInitial(): 'light' | 'dark' {
    if (!this.isBrowser()) return 'light';
    const saved = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (saved) return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  private apply(theme: 'light' | 'dark') {
    if (!this.isBrowser()) return;
    document.documentElement.setAttribute('data-theme', theme);
  }
  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }
}
