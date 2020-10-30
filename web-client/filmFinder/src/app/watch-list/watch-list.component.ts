import {Component, Input, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {UserMessageConstant} from '../constants/UserMessageConstant';

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
  onClick(): void{
    this.webService.watchlist(this.movieID).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.WATCH_LIST_ADDED, UserMessageConstant.DISMISS);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.WATCH_LIST_ADD_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }

  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
