import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExperimentsPage } from './experiments-page';

describe('ExperimentsPage', () => {
  let component: ExperimentsPage;
  let fixture: ComponentFixture<ExperimentsPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExperimentsPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExperimentsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
