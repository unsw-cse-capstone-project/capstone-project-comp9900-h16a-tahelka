import {Component, Input, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {UserMessageConstant} from '../constants/UserMessageConstant';

@Component({
  selector: 'app-subscribe',
  templateUrl: './subscribe.component.html',
  styleUrls: ['./subscribe.component.css']
})
export class SubscribeComponent implements OnInit {

  @Input() public userID;
  public subscribed = true;
  snackbarDuration = 2000;
  constructor(private webService: WebService,
              private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  subscribe(): void {
      this.webService.subscribeUser(this.userID).subscribe(success => {
        this.successfulUpdateSnackbar(UserMessageConstant.SUBSCRIBED_USER, UserMessageConstant.DISMISS);
      }, err => {
        this.successfulUpdateSnackbar(UserMessageConstant.SUBSCRIBED_USER_UNSUCCESSFUL, UserMessageConstant.DISMISS);
      });
      this.subscribed = false;
    }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
