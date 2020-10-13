import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrowseGenreComponent } from './browse-genre.component';

describe('BrowseGenreComponent', () => {
  let component: BrowseGenreComponent;
  let fixture: ComponentFixture<BrowseGenreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrowseGenreComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BrowseGenreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
