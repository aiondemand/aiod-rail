import { AfterViewInit, Component, ElementRef, Input, OnChanges, SimpleChanges, ViewChild } from '@angular/core';

@Component({
  selector: 'app-base-doc',
  templateUrl: './base-doc.component.html',
  styleUrls: ['./base-doc.component.scss']
})
export class BaseDocComponent implements AfterViewInit {
  @Input() showToc: boolean = true;

  @ViewChild('content', { static: false }) contentDiv: ElementRef;

  headers: HTMLHeadingElement[] = [];

  ngAfterViewInit(): void {
    let div = this.contentDiv.nativeElement as HTMLDivElement;

    // select all h1 and h2 elements inside div element
    let headers = div.querySelectorAll('h1, h2');
    this.headers = Array.from(headers) as HTMLHeadingElement[];
    this.headers.forEach(header => {
      header.addEventListener('click', () => {
        this.scrollToHeader(header);
      });
    });
  }

  scrollToHeader(header: HTMLHeadingElement): void {
    header.scrollIntoView({ behavior: 'smooth' });
  }
}
