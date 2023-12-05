import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentTemplateListItemComponent } from './experiment-template-list-item.component';

describe('ExperimentTemplateListItemComponent', () => {
  let component: ExperimentTemplateListItemComponent;
  let fixture: ComponentFixture<ExperimentTemplateListItemComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExperimentTemplateListItemComponent]
    });
    fixture = TestBed.createComponent(ExperimentTemplateListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
