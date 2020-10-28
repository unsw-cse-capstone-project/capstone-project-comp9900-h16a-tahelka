import { Component, OnInit } from '@angular/core';
import {WebService} from '../services/web.service';
import {BannedUser} from '../models/BannedUser';
import {SubscribedUser} from '../models/SubscribedUser';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-banned-user-list',
  templateUrl: './banned-user-list.component.html',
  styleUrls: ['./banned-user-list.component.css']
})
export class BannedUserListComponent implements OnInit {
  dataSource: BannedUser[];
  displayedColumns: string[] = ['username', 'unblock'];
  snackbarDuration = 2000;
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
    this.getData();
  }
  getData(): void {
    this.webService.getBannedUserList().subscribe(success => {
      this.dataSource = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
  onClick(bannedUser: BannedUser): void{
    this.webService.unBannedUser(bannedUser.userID).subscribe(success => {
      this.dataSource = this.dataSource.filter(obj => obj !== bannedUser);
      this.successfulUpdateSnackbar(UserMessageConstant.UNBAN_SUCCESSFUL, UserMessageConstant.DISMISS);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.UNBAN_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }

  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}
