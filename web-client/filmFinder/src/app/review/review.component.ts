import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {


  public selectedRating: number;
  reviewForm = new FormGroup({
    givenRating: new FormControl('', [Validators.required]),
    givenReview: new FormControl('', [Validators.required])
  });
  @Output() private ratingNew = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }
  saveClick(): void {
    console.log('Review Saved');
    console.log(this.reviewForm.value);
  }
}
