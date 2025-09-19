import { CommonModule, isPlatformBrowser } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  ViewEncapsulation,
  AfterViewInit,
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
export class BaseDocComponent implements AfterViewInit {
  constructor(
    private host: ElementRef<HTMLElement>,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  async ngAfterViewInit() {
    if (!isPlatformBrowser(this.platformId)) return;

    // Prism + jazyk(y) načítaj len v prehliadači
    const prismMod = await import('prismjs');
    const Prism: any = (prismMod as any).default ?? prismMod;
    await import('prismjs/components/prism-python');
    await import('prismjs/components/prism-properties');
    await import('prismjs/components/prism-json');

    Prism.highlightAllUnder(this.host.nativeElement);
  }
}
