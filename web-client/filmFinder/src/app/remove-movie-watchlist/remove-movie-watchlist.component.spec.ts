import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RemoveMovieWatchlistComponent } from './remove-movie-watchlist.component';

describe('RemoveMovieWatchlistComponent', () => {
  let component: RemoveMovieWatchlistComponent;
  let fixture: ComponentFixture<RemoveMovieWatchlistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RemoveMovieWatchlistComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RemoveMovieWatchlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
