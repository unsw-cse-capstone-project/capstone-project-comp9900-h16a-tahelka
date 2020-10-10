import {Component, Input, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-watch-list',
  templateUrl: './watch-list.component.html',
  styleUrls: ['./watch-list.component.css']
})
export class WatchListComponent implements OnInit {

  @Input() public movie;
  movieId: number;
  snackbarDuration = 2000;
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  onClick(message, action): void{
    const snackbarRef =  this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {
      console.log('The snackbar was dismissed');
    });

    console.log('Added to watch-list');
    this.movieId = this.movie;
    this.webService.watchlist(this.movieId).subscribe(success => {
      this.movieId = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
