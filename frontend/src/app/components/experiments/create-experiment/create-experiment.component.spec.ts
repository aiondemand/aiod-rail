import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateExperimentComponent } from './create-experiment.component';

describe('CreateExperimentComponent', () => {
  let component: CreateExperimentComponent;
  let fixture: ComponentFixture<CreateExperimentComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateExperimentComponent]
    });
    fixture = TestBed.createComponent(CreateExperimentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
