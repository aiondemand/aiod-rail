import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent implements AfterViewInit {
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
