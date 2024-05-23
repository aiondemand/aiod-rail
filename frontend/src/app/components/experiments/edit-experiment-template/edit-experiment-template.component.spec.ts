import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditExperimentTemplateComponent } from './edit-experiment-template.component';

describe('EditExperimentTemplateComponent', () => {
  let component: EditExperimentTemplateComponent;
  let fixture: ComponentFixture<EditExperimentTemplateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [EditExperimentTemplateComponent]
    });
    fixture = TestBed.createComponent(EditExperimentTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
