import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubscribedUserListComponent } from './subscribed-user-list.component';

describe('SubscribedUserListComponent', () => {
  let component: SubscribedUserListComponent;
  let fixture: ComponentFixture<SubscribedUserListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SubscribedUserListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubscribedUserListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
