import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatasetDetailComponent } from './dataset-detail.component';

describe('DatasetDetailComponent', () => {
  let component: DatasetDetailComponent;
  let fixture: ComponentFixture<DatasetDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DatasetDetailComponent]
    });
    fixture = TestBed.createComponent(DatasetDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
