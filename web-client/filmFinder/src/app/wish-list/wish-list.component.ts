import {Component, Input, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-wish-list',
  templateUrl: './wish-list.component.html',
  styleUrls: ['./wish-list.component.css']
})
export class WishListComponent implements OnInit {

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

    console.log('Added to wish-list');
    this.movieId = this.movie;
    this.webService.wishlist(this.movieId).subscribe(success => {
      this.movieId = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
