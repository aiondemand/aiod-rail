import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SavedDatasetsComponent } from './saved-datasets.component';

describe('SavedDatasetsComponent', () => {
  let component: SavedDatasetsComponent;
  let fixture: ComponentFixture<SavedDatasetsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SavedDatasetsComponent]
    });
    fixture = TestBed.createComponent(SavedDatasetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
