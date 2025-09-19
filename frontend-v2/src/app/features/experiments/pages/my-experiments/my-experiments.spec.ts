import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyExperiments } from './my-experiments';

describe('MyExperiments', () => {
  let component: MyExperiments;
  let fixture: ComponentFixture<MyExperiments>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyExperiments]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyExperiments);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
