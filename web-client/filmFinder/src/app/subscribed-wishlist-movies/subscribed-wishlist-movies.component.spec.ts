import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubscribedWishlistMoviesComponent } from './subscribed-wishlist-movies.component';

describe('SubscribedWishlistMoviesComponent', () => {
  let component: SubscribedWishlistMoviesComponent;
  let fixture: ComponentFixture<SubscribedWishlistMoviesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SubscribedWishlistMoviesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubscribedWishlistMoviesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
