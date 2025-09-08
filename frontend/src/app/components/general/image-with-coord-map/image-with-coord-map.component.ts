import { AfterContentChecked, Component, ElementRef } from '@angular/core';

@Component({
  selector: 'app-image-with-coord-map',
  templateUrl: './image-with-coord-map.component.html',
  styleUrls: ['./image-with-coord-map.component.scss']
})
export class ImageWithCoordMapComponent implements AfterContentChecked {

  constructor(private thisElement: ElementRef) { }

  ngAfterContentChecked(): void {
    if (!this.thisElement || !this.thisElement.nativeElement) {
      return;
    }

    let image = this.thisElement.nativeElement.querySelector('img') as HTMLImageElement;
    let map = this.thisElement.nativeElement.querySelector('map') as HTMLMapElement;

    if (!image || !map) {
      return;
    }

    let widthRatio = image.width / image.naturalWidth;
    let heightRatio = image.height / image.naturalHeight;


    if (image.width === 0 || image.height === 0 || image.naturalWidth === 0 || image.naturalHeight === 0) {
      return;
    }

    // Don't rescale if the image is shown in its original size
    if (widthRatio === 1 && heightRatio === 1) {
      return;
    }

    let areas = map.querySelectorAll('area') as NodeListOf<HTMLAreaElement>;
    areas.forEach(area => {
      if (!area.hasAttribute("originalCoords")) {
        area.setAttribute("originalCoords", area.coords);
      }

      let coords = (area.getAttribute("originalCoords") || '').split(',');
      let newCoords = coords.map(coord => {
        if (coords.indexOf(coord) % 2 === 0) {
          return String(Number(coord) * widthRatio);
        } else {
          return String(Number(coord) * heightRatio);
        }
      });
      area.coords = newCoords.join(',');
    });
  }
}
