import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IntegrateWishlistComponent } from './integrate-wishlist.component';

describe('IntegrateWishlistComponent', () => {
  let component: IntegrateWishlistComponent;
  let fixture: ComponentFixture<IntegrateWishlistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IntegrateWishlistComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IntegrateWishlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
