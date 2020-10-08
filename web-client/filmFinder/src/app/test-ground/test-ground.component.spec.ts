import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestGroundComponent } from './test-ground.component';

describe('TestGroundComponent', () => {
  let component: TestGroundComponent;
  let fixture: ComponentFixture<TestGroundComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestGroundComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TestGroundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
