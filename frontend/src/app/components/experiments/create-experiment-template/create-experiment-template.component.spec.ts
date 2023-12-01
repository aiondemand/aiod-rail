import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateExperimentTemplateComponent } from './create-experiment-template.component';

describe('CreateExperimentTemplateComponent', () => {
  let component: CreateExperimentTemplateComponent;
  let fixture: ComponentFixture<CreateExperimentTemplateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateExperimentTemplateComponent]
    });
    fixture = TestBed.createComponent(CreateExperimentTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
