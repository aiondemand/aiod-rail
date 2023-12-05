import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentTemplateDetailComponent } from './experiment-template-detail.component';

describe('ExperimentTemplateDetailComponent', () => {
  let component: ExperimentTemplateDetailComponent;
  let fixture: ComponentFixture<ExperimentTemplateDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExperimentTemplateDetailComponent]
    });
    fixture = TestBed.createComponent(ExperimentTemplateDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
