import {Component, Input, OnInit} from '@angular/core';
import {MovieReview} from '../models/MovieReview';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {UserMessageConstant} from '../constants/UserMessageConstant';

@Component({
  selector: 'app-review-list',
  templateUrl: './review-list.component.html',
  styleUrls: ['./review-list.component.css']
})
export class ReviewListComponent implements OnInit {

  @Input() movieID: number;
  movieReviewsSource: MovieReview[];
  snackbarDuration = 2000;
  columnsToDisplay: string[] = ['username', 'rating', 'review', 'block'];
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  setMovieReviews(event: MovieReview[]): void {
    this.movieReviewsSource = event;
  }
  // block users http call
  blockUser(event: MovieReview): void {
    this.webService.blockUser(event.userID).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.BLOCKED_USER_SUCCESSFUL, UserMessageConstant.DISMISS);
      // remove user in the list on successful calls
      this.movieReviewsSource = this.movieReviewsSource.filter(obj => obj !== event);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.BLOCKED_USER_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
