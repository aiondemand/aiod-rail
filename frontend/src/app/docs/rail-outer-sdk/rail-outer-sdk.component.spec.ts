import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RailOuterSdkComponent } from './rail-outer-sdk.component';

describe('RailOuterSdkComponent', () => {
  let component: RailOuterSdkComponent;
  let fixture: ComponentFixture<RailOuterSdkComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RailOuterSdkComponent]
    });
    fixture = TestBed.createComponent(RailOuterSdkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
