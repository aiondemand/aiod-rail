import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RailSDKs } from './rail-sdks';

describe('RailSDKs', () => {
  let component: RailSDKs;
  let fixture: ComponentFixture<RailSDKs>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RailSDKs]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RailSDKs);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
