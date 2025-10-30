import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateTemplate } from './create-template';

describe('CreateTemplate', () => {
  let component: CreateTemplate;
  let fixture: ComponentFixture<CreateTemplate>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateTemplate]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateTemplate);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
