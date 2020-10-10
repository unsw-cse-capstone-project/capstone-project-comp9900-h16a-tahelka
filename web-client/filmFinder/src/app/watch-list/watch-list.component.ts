import {Component, Input, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-watch-list',
  templateUrl: './watch-list.component.html',
  styleUrls: ['./watch-list.component.css']
})
export class WatchListComponent implements OnInit {

  @Input() public movieID: number;
  snackbarDuration = 2000;
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  onClick(message, action): void{

    console.log('Added to watch-list');
    this.webService.watchlist(this.movieID).subscribe(success => {
      console.log(success);
      this.successfulUpdateSnackbar(message, action);
    }, err => {
      alert(JSON.stringify(err));
    });
  }

  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {
      console.log('The snackbar was dismissed');
    });
  }
}
