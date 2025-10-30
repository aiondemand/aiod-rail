import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainConceptsRunPage } from './main-concepts-run-page';

describe('MainConceptsRunPage', () => {
  let component: MainConceptsRunPage;
  let fixture: ComponentFixture<MainConceptsRunPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainConceptsRunPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MainConceptsRunPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
