import {Component, Input, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {UserMessageConstant} from '../constants/UserMessageConstant';

@Component({
  selector: 'app-wish-list',
  templateUrl: './wish-list.component.html',
  styleUrls: ['./wish-list.component.css']
})
export class WishListComponent implements OnInit {

  @Input() public movieID: number;
  snackbarDuration = 2000;
  addedToWishlistMessage = UserMessageConstant.WISH_LIST_ADDED;
  dismissMessage = UserMessageConstant.DISMISS;
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  onClick(message, action): void{
    this.webService.wishlist(this.movieID).subscribe(success => {
      console.log(success);
      this.successfulUpdateSnackbar(message, action);
    }, err => {
      alert(JSON.stringify(err));
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
