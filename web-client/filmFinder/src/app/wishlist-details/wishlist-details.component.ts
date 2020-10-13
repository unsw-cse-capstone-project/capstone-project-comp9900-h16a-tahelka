import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {WebService} from '../services/web.service';

@Component({
  selector: 'app-wishlist-details',
  templateUrl: './wishlist-details.component.html',
  styleUrls: ['./wishlist-details.component.css']
})
export class WishlistDetailsComponent implements OnInit {
  // TODO: Create model
  result: any;
  constructor(private route: ActivatedRoute, private webService: WebService) { }
  id: number;
  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.id = params.id;
    });
    if (this.id === undefined) {
      this.id = -1;
    }
    this.getData(this.id);
  }
  getData(id: number): void {
    this.webService.wishListDetails(id).subscribe(success => {
      this.result = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
