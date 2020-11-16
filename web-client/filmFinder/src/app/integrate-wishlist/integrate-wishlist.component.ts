import {Component, Input, OnInit} from '@angular/core';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthenticationService} from '../services/authentication.service';

@Component({
  selector: 'app-integrate-wishlist',
  templateUrl: './integrate-wishlist.component.html',
  styleUrls: ['./integrate-wishlist.component.css']
})
export class IntegrateWishlistComponent implements OnInit {
  @Input() userID: number;
  snackbarDuration = 2000;
  constructor(private webService: WebService,
              private snackbar: MatSnackBar,
              private router: Router,
              private route: ActivatedRoute,
              private authenticationService: AuthenticationService) { }

  ngOnInit(): void {
  }
  // http call to import wishlist
  wishlistImport(): void{
    this.webService.wishlistImport(this.userID).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.WISHLIST_IMPORT_SUCCESSFUL, UserMessageConstant.DISMISS);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.WISHLIST_IMPORT_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
