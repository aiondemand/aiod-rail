import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HuggingfaceFormComponent } from './huggingface-form.component';

describe('HuggingfaceFormComponent', () => {
  let component: HuggingfaceFormComponent;
  let fixture: ComponentFixture<HuggingfaceFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HuggingfaceFormComponent]
    });
    fixture = TestBed.createComponent(HuggingfaceFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
