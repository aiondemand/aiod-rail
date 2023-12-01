import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateDatasetComponent } from './create-dataset.component';

describe('CreateDatasetComponent', () => {
  let component: CreateDatasetComponent;
  let fixture: ComponentFixture<CreateDatasetComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateDatasetComponent]
    });
    fixture = TestBed.createComponent(CreateDatasetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
