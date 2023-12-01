import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatasetListItemComponent } from './dataset-list-item.component';

describe('DatasetListItemComponent', () => {
  let component: DatasetListItemComponent;
  let fixture: ComponentFixture<DatasetListItemComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DatasetListItemComponent]
    });
    fixture = TestBed.createComponent(DatasetListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
