import { AfterContentChecked, AfterContentInit, AfterViewChecked, AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'app-base-doc',
  templateUrl: './base-doc.component.html',
  styleUrls: ['./base-doc.component.scss']
})
export class BaseDocComponent implements AfterContentChecked {
  @ViewChild('content', { static: true }) contentDiv: ElementRef;

  headers: HTMLHeadingElement[] = [];

  ngAfterContentChecked(): void {
    if (!this.contentDiv) {
      return;
    }

    let div = this.contentDiv.nativeElement as HTMLDivElement;

    // select all h1 and h2 elements inside div element
    let headers = Array.from(div.querySelectorAll('h1, h2')) as HTMLHeadingElement[];

    // if headers are the same, return, don't reinitialize
    if (this.headers.length === headers.length && this.headers.every((v, i) => v === headers[i])) {
      return;
    }

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
