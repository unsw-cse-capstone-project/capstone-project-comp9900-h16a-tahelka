import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {WebService} from '../services/web.service';
import {AuthenticationService} from '../services/authentication.service';
import {WishlistDetails} from '../models/WishlistDetails';

@Component({
  selector: 'app-wishlist-details',
  templateUrl: './wishlist-details.component.html',
  styleUrls: ['./wishlist-details.component.css']
})
export class WishlistDetailsComponent implements OnInit {
  result: WishlistDetails;
  constructor(private route: ActivatedRoute, private webService: WebService, private authenticationService: AuthenticationService) { }
  id: number;
  showSubscribeButtons = true;
  showSubscribeButton = true;
  showUnsubscribeButton = true;
  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.id = params.id;
    });
    this.getData();
  }
  getData(): void {
    if (this.id === undefined) {
      this.id = this.authenticationService.currentUserValue.userID;
      this.showSubscribeButtons = false;
    }
    this.webService.wishListDetails(this.id).subscribe(success => {
      this.result = success;
      this.checkButtons();
    }, err => {
      alert(JSON.stringify(err));
    });
  }
  checkButtons(): void {
    if (this.result.isSubscribed === true) {
      this.subscribeSuccessful();
    } else if (this.result.isSubscribed === false) {
      this.unsubscribeSuccessful();
    }
  }
  subscribeSuccessful(): void {
      this.showSubscribeButton = false;
      this.showUnsubscribeButton = true;
  }
  unsubscribeSuccessful(): void {
      this.showSubscribeButton = true;
      this.showUnsubscribeButton = false;
  }
}
