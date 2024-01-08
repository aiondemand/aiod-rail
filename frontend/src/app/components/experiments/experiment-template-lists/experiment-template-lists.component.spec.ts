import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AllExperimentTemplateList } from './all-experiment-template-list.component';


describe('AllExperimentTemplateList', () => {
  let component: AllExperimentTemplateList;
  let fixture: ComponentFixture<AllExperimentTemplateList>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AllExperimentTemplateList]
    });
    fixture = TestBed.createComponent(AllExperimentTemplateList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
