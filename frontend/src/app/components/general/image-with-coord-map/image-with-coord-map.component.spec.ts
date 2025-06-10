import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageWithCoordMapComponent } from './image-with-coord-map.component';

describe('ImageWithCoordMapComponent', () => {
  let component: ImageWithCoordMapComponent;
  let fixture: ComponentFixture<ImageWithCoordMapComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ImageWithCoordMapComponent]
    });
    fixture = TestBed.createComponent(ImageWithCoordMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
