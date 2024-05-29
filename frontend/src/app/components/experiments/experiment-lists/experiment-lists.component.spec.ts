import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PublicExperimentListComponent } from './public-experiment-list.component';

describe('PublicExperimentListComponent', () => {
  let component: PublicExperimentListComponent;
  let fixture: ComponentFixture<PublicExperimentListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PublicExperimentListComponent]
    });
    fixture = TestBed.createComponent(PublicExperimentListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
