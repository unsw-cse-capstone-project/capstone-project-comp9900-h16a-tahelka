import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import {FormControl, FormGroup, FormGroupDirective, Validators} from '@angular/forms';
import {WebService} from '../services/web.service';
import {Review} from '../models/Review';
import {MatSnackBar} from '@angular/material/snack-bar';
import {UserMessageConstant} from '../constants/UserMessageConstant';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {

  @Input() movieId: number;
  snackbarDuration = 2000;
  reviewAddedMessage = UserMessageConstant.REVIEW_ADDED;
  dismissMessage = UserMessageConstant.DISMISS;

  review: Review;
  reviewForm = new FormGroup({
    rating: new FormControl(0, [Validators.required]),
    review: new FormControl('', [Validators.required])
  });

  constructor(private webService: WebService, private snackbar: MatSnackBar) {}

  ngOnInit(): void {
  }
  saveClick(fData: any, formDirective: FormGroupDirective): void {
    this.review = this.reviewForm.value;
    this.webService.review(this.review, this.movieId).subscribe(success => {
      this.successfulUpdateSnackbar(this.reviewAddedMessage, this.dismissMessage);
      this.reviewForm.reset();
      formDirective.resetForm();
    }, err => {
      alert(JSON.stringify(err));
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
