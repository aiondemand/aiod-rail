import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RailSdksComponent } from './rail-sdks.component';

describe('RailSdksComponent', () => {
  let component: RailSdksComponent;
  let fixture: ComponentFixture<RailSdksComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RailSdksComponent]
    });
    fixture = TestBed.createComponent(RailSdksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
