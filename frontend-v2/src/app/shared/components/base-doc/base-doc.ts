import { CommonModule } from '@angular/common';
import {
  AfterViewInit,
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  OnDestroy,
  ViewEncapsulation,
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

  constructor(private host: ElementRef<HTMLElement>) {}

  private runHighlight = () => {
    const hljs = (window as any).hljs;
    if (!hljs) return;

    const root = this.host.nativeElement;
    const blocks = root.querySelectorAll<HTMLElement>(
      'pre code:not([data-hljs-done]):not(.language-properties)'
    ); //pre code:not([data-hljs-done])

    blocks.forEach((el) => {
      try {
        hljs.highlightElement(el);
        el.dataset['hljsDone'] = '1';
        el.parentElement?.classList.add('hljs');
      } catch {
        // ignore
      }
    });
  };

  ngAfterViewInit() {
    this.runHighlight();

    let scheduled = false;
    this.mo = new MutationObserver(() => {
      if (scheduled) return;
      scheduled = true;
      requestAnimationFrame(() => {
        scheduled = false;
        this.runHighlight();
      });
    });
    this.mo.observe(this.host.nativeElement, { childList: true, subtree: true });
  }

  ngOnDestroy() {
    this.mo?.disconnect();
  }
}
