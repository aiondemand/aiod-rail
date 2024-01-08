import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentRunListComponent } from './experiment-run-list.component';

describe('ExperimentRunListComponent', () => {
  let component: ExperimentRunListComponent;
  let fixture: ComponentFixture<ExperimentRunListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExperimentRunListComponent]
    });
    fixture = TestBed.createComponent(ExperimentRunListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
