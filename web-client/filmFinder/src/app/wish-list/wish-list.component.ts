import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {ActivatedRoute, Router} from '@angular/router';
import {Recommendations} from '../models/Recommendations';
import {WishlistRemove} from '../models/WishlistRemove';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-wish-list',
  templateUrl: './wish-list.component.html',
  styleUrls: ['./wish-list.component.css']
})
export class WishListComponent implements OnInit {

  @Input() public movieID: number;
  snackbarDuration = 2000;
  @Output() deleteFromWishlist = new EventEmitter<WishlistRemove>();
  isWishlistDetails = false;
  id: number;
  showDelete = false;
  constructor(private webService: WebService,
              private snackbar: MatSnackBar,
              private router: Router,
              private route: ActivatedRoute,
              private authenticationService: AuthenticationService) { }

  ngOnInit(): void {
    if (this.router.url.startsWith('/wishlist')) {
      this.isWishlistDetails = true;
    }
    this.route.params.subscribe(params => {
      this.id = params?.id;
      if (this.id !== undefined) {
        this.isWishlistDetails = false;
      }
    });
    this.setRemoveButtonView();
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
      if (this.isWishlistDetails) {
        this.deleteFromWishlist.emit({movieID: this.movieID, route: 'wishlist'});
      }
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.WISHLIST_REMOVE_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
  setRemoveButtonView(): void {
    if (this.id === undefined || +this.id === this.authenticationService.currentUserValue.userID) {
      this.showDelete = true;
    }
  }
}
