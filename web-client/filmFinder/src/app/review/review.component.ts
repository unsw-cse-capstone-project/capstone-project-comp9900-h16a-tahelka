import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {WebService} from '../services/web.service';
import {Review} from '../models/Review';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {

  @Input() movieId: number;
  review: Review;
  reviewForm = new FormGroup({
    givenRating: new FormControl('', [Validators.required]),
    givenReview: new FormControl('', [Validators.required])
  });

  constructor(private webService: WebService) {}

  ngOnInit(): void {
  }
  saveClick(): void {
    console.log('Review Saved');
    this.review = this.reviewForm.value;
    this.webService.review(this.review, this.movieId).subscribe(success => {
      this.review = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
