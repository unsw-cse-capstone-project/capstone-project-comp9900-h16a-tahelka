import { Component, OnInit } from '@angular/core';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {MovieResult} from '../models/MovieResult';

@Component({
  selector: 'app-watched-movies',
  templateUrl: './watched-movies.component.html',
  styleUrls: ['./watched-movies.component.css']
})
export class WatchedMoviesComponent implements OnInit {
  snackbarDuration = 2000;
  datasource: MovieResult[];
  constructor(private webService: WebService,
              private snackbar: MatSnackBar) { }

  ngOnInit(): void {
    this.getData();
  }
  getData(): void{
    this.webService.getWatchlist().subscribe(success => {
      this.datasource = success.watchlist;
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
