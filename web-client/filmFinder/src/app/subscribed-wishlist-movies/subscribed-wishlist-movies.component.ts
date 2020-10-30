import { Component, OnInit } from '@angular/core';
import { SubscribedWishlistMoviesResult } from '../models/SubscribedWishlistMoviesResult';
import {WebService} from '../services/web.service';

@Component({
  selector: 'app-subscribed-wishlist-movies',
  templateUrl: './subscribed-wishlist-movies.component.html',
  styleUrls: ['./subscribed-wishlist-movies.component.css']
})
export class SubscribedWishlistMoviesComponent implements OnInit {
  displayedColumns: string[] = ['username', 'title'];
  dataSource: SubscribedWishlistMoviesResult[];
  constructor(private webService: WebService) { }

  ngOnInit(): void {
    this.getData();
  }
  getData(): void {
    this.webService.getSubscribedWishlistMovies().subscribe(success => {
      this.dataSource = success.movies;
    }, err => {
      alert(err);
    });
  }
}
