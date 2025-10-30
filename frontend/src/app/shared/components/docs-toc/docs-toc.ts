import { CommonModule, DOCUMENT, isPlatformBrowser } from '@angular/common';
import {
  AfterViewInit,
  ChangeDetectionStrategy,
  Component,
  Input,
  OnDestroy,
  PLATFORM_ID,
  inject,
  signal,
} from '@angular/core';

export type TocItem = { id: string; text: string; level: 1 | 2 | 3 };

@Component({
  selector: 'app-docs-toc',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './docs-toc.html',
  styleUrls: ['./docs-toc.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DocsTocComponent implements AfterViewInit, OnDestroy {
  @Input() container: string = '.doc-content';

  private platformId = inject(PLATFORM_ID);
  private isBrowser = isPlatformBrowser(this.platformId);
  private doc = inject(DOCUMENT);

  items = signal<TocItem[]>([]);
  activeId = signal<string>('');

  private io?: IntersectionObserver;
  private mo?: MutationObserver;

  ngAfterViewInit(): void {
    if (!this.isBrowser) return;

    const root = this.doc.querySelector(this.container) as HTMLElement | null;
    if (!root) return;

    this.buildToc(root);

    this.mo = new MutationObserver(() => {
      this.buildToc(root);
      this.setupActiveObserver(root);
    });
    this.mo.observe(root, { childList: true, subtree: true });

    this.setupActiveObserver(root);
  }

  ngOnDestroy(): void {
    if (!this.isBrowser) return;
    this.io?.disconnect();
    this.mo?.disconnect();
  }

  private buildToc(root: HTMLElement) {
    const hs = Array.from(root.querySelectorAll('h1, h2, h3')) as HTMLHeadingElement[];

    hs.forEach((h) => {
      if (!h.id) {
        const slug = (h.textContent ?? '')
          .toLowerCase()
          .trim()
          .replace(/[^\w\- ]+/g, '')
          .replace(/\s+/g, '-');
        h.id = slug || `section-${Math.random().toString(36).slice(2, 8)}`;
      }
    });

    const items = hs.map((h) => ({
      id: h.id,
      text: (h.textContent || '').trim(),
      level: (h.tagName.toLowerCase() === 'h1' ? 1 : h.tagName.toLowerCase() === 'h2' ? 2 : 3) as
        | 1
        | 2
        | 3,
    }));

    this.items.set(items);
  }

  private setupActiveObserver(root: HTMLElement) {
    const secs = Array.from(root.querySelectorAll('h1, h2, h3')) as HTMLElement[];
    if (!secs.length) return;

    this.io?.disconnect();
    this.io = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort(
            (a, b) => (a.target as HTMLElement).offsetTop - (b.target as HTMLElement).offsetTop
          )[0]?.target as HTMLElement | undefined;

        if (visible?.id) this.activeId.set(visible.id);
      },
      { rootMargin: '-20% 0px -70% 0px', threshold: [0, 1] }
    );

    secs.forEach((s) => this.io!.observe(s));
  }

  scrollTo(id: string, ev: Event) {
    if (!this.isBrowser) return;
    ev.preventDefault();
    const el = this.doc.getElementById(id);
    if (!el) return;
    window.scrollTo({
      top: el.getBoundingClientRect().top + window.scrollY - 80,
      behavior: 'smooth',
    });
    history.replaceState(null, '', `#${id}`);
  }
}
