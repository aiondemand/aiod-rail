import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateExperiment } from './create-experiment';

describe('CreateExperiment', () => {
  let component: CreateExperiment;
  let fixture: ComponentFixture<CreateExperiment>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateExperiment]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateExperiment);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
