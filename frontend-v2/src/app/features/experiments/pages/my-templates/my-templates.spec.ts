import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyTemplates } from './my-templates';

describe('MyTemplates', () => {
  let component: MyTemplates;
  let fixture: ComponentFixture<MyTemplates>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyTemplates]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyTemplates);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
