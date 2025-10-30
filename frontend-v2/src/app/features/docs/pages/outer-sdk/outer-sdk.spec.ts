import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OuterSDK } from './outer-sdk';

describe('OuterSDK', () => {
  let component: OuterSDK;
  let fixture: ComponentFixture<OuterSDK>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OuterSDK]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OuterSDK);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
