import { CommonModule, isPlatformBrowser } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  ViewEncapsulation,
  AfterViewInit,
  OnDestroy,
  ElementRef,
  Inject,
  PLATFORM_ID,
} from '@angular/core';
import { DocsTocComponent } from '../docs-toc/docs-toc';

@Component({
  selector: 'app-base-doc',
  standalone: true,
  imports: [CommonModule, DocsTocComponent],
  templateUrl: './base-doc.html',
  styleUrls: ['./base-doc.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.None,
})
export class BaseDocComponent implements AfterViewInit, OnDestroy {
  private mo?: MutationObserver;
  private Prism: any;

  constructor(
    private host: ElementRef<HTMLElement>,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  async ngAfterViewInit() {
    if (!isPlatformBrowser(this.platformId)) return;
    const Prism = (window as any).Prism;
    const root = this.host.nativeElement;
    const highlight = () => Prism?.highlightAllUnder?.(root);

    highlight();

    let scheduled = false;
    this.mo = new MutationObserver(() => {
      if (scheduled) return;
      scheduled = true;
      requestAnimationFrame(() => {
        scheduled = false;
        highlight();
      });
    });
    this.mo.observe(root, { childList: true, subtree: true });
  }

  ngOnDestroy() {
    this.mo?.disconnect();
  }
}
