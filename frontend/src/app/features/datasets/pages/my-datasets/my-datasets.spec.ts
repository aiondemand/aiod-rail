import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyDatasets } from './my-datasets';

describe('MyDatasets', () => {
  let component: MyDatasets;
  let fixture: ComponentFixture<MyDatasets>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyDatasets]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyDatasets);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
