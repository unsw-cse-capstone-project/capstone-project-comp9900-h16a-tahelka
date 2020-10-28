import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BannedUserListComponent } from './banned-user-list.component';

describe('BannedUserListComponent', () => {
  let component: BannedUserListComponent;
  let fixture: ComponentFixture<BannedUserListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BannedUserListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BannedUserListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
