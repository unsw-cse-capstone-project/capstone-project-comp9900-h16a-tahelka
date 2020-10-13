import {Component, Input, OnInit} from '@angular/core';
import {Recommendations} from '../models/Recommendations';
import {MovieReview} from '../models/MovieReview';
import {Router} from '@angular/router';

@Component({
  selector: 'app-review-list',
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.css']
})
export class ReviewListComponent implements OnInit {

  @Input() movieID: number;
  movieReviewsSource: MovieReview[];
  columnsToDisplay: string[] = ['username', 'rating', 'review'];
  constructor(private router: Router) { }

  ngOnInit(): void {
  }
  setMovieReviews(event: MovieReview[]): void {
    this.movieReviewsSource = event;
  }
  navigate(id: number): void {
    const pathToNavigate = 'wishlist/' + id.toString();
    console.log(pathToNavigate);
    this.router.navigate([pathToNavigate]);
  }

}
