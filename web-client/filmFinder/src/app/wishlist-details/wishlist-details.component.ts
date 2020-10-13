import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-wishlist-details',
  templateUrl: './wishlist-details.component.html',
  styleUrls: ['./wishlist-details.component.css']
})
export class WishlistDetailsComponent implements OnInit {

  constructor(private route: ActivatedRoute) { }
  id: number;
  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.id = params.id;
    });
  }

}
