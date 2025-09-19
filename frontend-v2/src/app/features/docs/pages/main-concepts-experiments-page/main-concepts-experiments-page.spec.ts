import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainConceptsExperimentsPage } from './main-concepts-experiments-page';

describe('MainConceptsExperimentsPage', () => {
  let component: MainConceptsExperimentsPage;
  let fixture: ComponentFixture<MainConceptsExperimentsPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainConceptsExperimentsPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MainConceptsExperimentsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
