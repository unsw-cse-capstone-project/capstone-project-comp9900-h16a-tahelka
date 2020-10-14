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
  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.id = params.id;
    });
    this.getData();
  }
  getData(): void {
    if (this.id === undefined) {
      this.id = this.authenticationService.currentUserValue.userID;
    }
    this.webService.wishListDetails(this.id).subscribe(success => {
      this.result = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
