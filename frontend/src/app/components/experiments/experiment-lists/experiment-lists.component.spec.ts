import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AllExperimentListComponent } from './all-experiment-list.component';

describe('AllExperimentListComponent', () => {
  let component: AllExperimentListComponent;
  let fixture: ComponentFixture<AllExperimentListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AllExperimentListComponent]
    });
    fixture = TestBed.createComponent(AllExperimentListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
