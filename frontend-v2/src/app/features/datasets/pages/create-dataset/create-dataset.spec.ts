import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateDataset } from './create-dataset';

describe('CreateDataset', () => {
  let component: CreateDataset;
  let fixture: ComponentFixture<CreateDataset>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateDataset]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateDataset);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
