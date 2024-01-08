import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentListItemComponent } from './experiment-list-item.component';

describe('ExperimentListItemComponent', () => {
  let component: ExperimentListItemComponent;
  let fixture: ComponentFixture<ExperimentListItemComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExperimentListItemComponent]
    });
    fixture = TestBed.createComponent(ExperimentListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
