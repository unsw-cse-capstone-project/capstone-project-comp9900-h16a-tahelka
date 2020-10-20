import {Component, Input, OnInit} from '@angular/core';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-unsubscribe',
  templateUrl: './unsubscribe.component.html',
  styleUrls: ['./unsubscribe.component.css']
})
export class UnsubscribeComponent implements OnInit {
  snackbarDuration = 2000;
  @Input() userID: number;
  constructor(private webService: WebService,
              private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  unsubscribe(): void {
    this.webService.unsubscribeUser(this.userID).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.UNSUBSCRIBED_USER, UserMessageConstant.DISMISS);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.UNSUBSCRIBED_USER_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
