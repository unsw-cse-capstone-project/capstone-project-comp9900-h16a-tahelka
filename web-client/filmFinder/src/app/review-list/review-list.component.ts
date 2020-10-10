import {Component, Input, OnInit} from '@angular/core';
import {Recommendations} from '../models/Recommendations';
import {MovieReview} from '../models/MovieReview';

@Component({
  selector: 'app-review-list',
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.css']
})
export class ReviewListComponent implements OnInit {

  @Input() movieID: number;
  movieReviewsSource: MovieReview[];
  columnsToDisplay: string[] = ['username', 'rating', 'review'];
  constructor() { }

  ngOnInit(): void {
  }
  setMovieReviews(event: MovieReview[]): void {
    this.movieReviewsSource = event;
  }

}
