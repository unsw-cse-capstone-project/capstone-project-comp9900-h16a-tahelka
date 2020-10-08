import { Component, Output, EventEmitter, OnInit } from '@angular/core';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {


  public selectedRating: number;
  @Output() private ratingNew = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }
  saveClick(): void {
    console.log('Review Saved');
  }
  cancelClick(): void {
    console.log('Review Canceled')
  }
}
