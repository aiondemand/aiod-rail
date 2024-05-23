import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PublicExperimentTemplateListComponent } from './public-experiment-template-list.component';


describe('PublicExperimentTemplateList', () => {
  let component: PublicExperimentTemplateListComponent;
  let fixture: ComponentFixture<PublicExperimentTemplateListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PublicExperimentTemplateListComponent]
    });
    fixture = TestBed.createComponent(PublicExperimentTemplateListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
