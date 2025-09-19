import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InnerSDK } from './inner-sdk';

describe('InnerSDK', () => {
  let component: InnerSDK;
  let fixture: ComponentFixture<InnerSDK>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InnerSDK]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InnerSDK);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
