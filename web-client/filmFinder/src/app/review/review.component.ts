import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import {FormControl, FormGroup, FormGroupDirective, Validators} from '@angular/forms';
import {WebService} from '../services/web.service';
import {Review} from '../models/Review';
import {MatSnackBar} from '@angular/material/snack-bar';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {Recommendations} from '../models/Recommendations';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {

  @Input() movieId: number;
  snackbarDuration = 2000;
  review: Review;
  @Output() reviewAdded = new EventEmitter<boolean>();
  reviewForm = new FormGroup({
    rating: new FormControl(null, [Validators.required]),
    review: new FormControl('', [Validators.required])
  });

  constructor(private webService: WebService, private snackbar: MatSnackBar) {}

  ngOnInit(): void {
  }
  // http method to add review
  saveClick(fData: any, formDirective: FormGroupDirective): void {
    this.review = this.reviewForm.value;
    this.webService.review(this.review, this.movieId).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.REVIEW_ADDED, UserMessageConstant.DISMISS);
      this.reviewForm.reset();
      // let parent know that review has been added, so it can load new reviews
      this.reviewAdded.emit(true);
      formDirective.resetForm();
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.REVIEW_ADD_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
