import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateExperimentComponent } from './update-experiment.component';

describe('UpdateExperimentComponent', () => {
  let component: UpdateExperimentComponent;
  let fixture: ComponentFixture<UpdateExperimentComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UpdateExperimentComponent]
    });
    fixture = TestBed.createComponent(UpdateExperimentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
