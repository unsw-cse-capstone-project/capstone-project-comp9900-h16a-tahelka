import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
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
  snackbarDuration = 2000;
  @Output() subscribed = new EventEmitter<boolean>();
  showSubscribeButton: boolean;
  constructor(private webService: WebService,
              private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  // http call to subscribe
  subscribe(): void {
      this.webService.subscribeUser(this.userID).subscribe(success => {
        this.successfulUpdateSnackbar(UserMessageConstant.SUBSCRIBED_USER, UserMessageConstant.DISMISS);
        // emit event to change button style
        this.subscribed.emit(true);
      }, err => {
        this.successfulUpdateSnackbar(UserMessageConstant.SUBSCRIBED_USER_UNSUCCESSFUL, UserMessageConstant.DISMISS);
      });
  }
  removeSubscribeButton(hide: boolean): void {

  }
  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
