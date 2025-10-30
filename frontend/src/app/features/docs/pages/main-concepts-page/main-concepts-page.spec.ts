import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainConceptsPage } from './main-concepts-page';

describe('MainConceptsPage', () => {
  let component: MainConceptsPage;
  let fixture: ComponentFixture<MainConceptsPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainConceptsPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MainConceptsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
