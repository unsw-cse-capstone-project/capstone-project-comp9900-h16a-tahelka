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
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  addToWishlist(): void{
    this.webService.wishlistAdd(this.movieID).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.WISHLIST_ADDED, UserMessageConstant.DISMISS);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.WISHLIST_ADD_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }
  removeFromWishlist(): void{
    this.webService.wishlistRemove(this.movieID).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.WISHLIST_REMOVED, UserMessageConstant.DISMISS);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.WISHLIST_REMOVE_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
