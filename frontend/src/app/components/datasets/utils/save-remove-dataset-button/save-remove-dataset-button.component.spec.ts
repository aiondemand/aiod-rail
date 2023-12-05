import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SaveRemoveDatasetButtonComponent } from './save-remove-dataset-button.component';

describe('SaveRemoveDatasetButtonComponent', () => {
  let component: SaveRemoveDatasetButtonComponent;
  let fixture: ComponentFixture<SaveRemoveDatasetButtonComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SaveRemoveDatasetButtonComponent]
    });
    fixture = TestBed.createComponent(SaveRemoveDatasetButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
