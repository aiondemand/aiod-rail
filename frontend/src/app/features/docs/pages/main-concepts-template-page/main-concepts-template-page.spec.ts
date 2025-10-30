import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainConceptsTemplatePage } from './main-concepts-template-page';

describe('MainConceptsTemplatePage', () => {
  let component: MainConceptsTemplatePage;
  let fixture: ComponentFixture<MainConceptsTemplatePage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainConceptsTemplatePage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MainConceptsTemplatePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
