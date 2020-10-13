import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrowseDirectorComponent } from './browse-director.component';

describe('BrowseDirectorComponent', () => {
  let component: BrowseDirectorComponent;
  let fixture: ComponentFixture<BrowseDirectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrowseDirectorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BrowseDirectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
