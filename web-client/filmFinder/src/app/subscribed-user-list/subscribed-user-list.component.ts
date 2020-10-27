import { Component, OnInit } from '@angular/core';
import {WebService} from '../services/web.service';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {SubscribedUser} from '../models/SubscribedUser';

@Component({
  selector: 'app-subscribed-user-list',
  templateUrl: './subscribed-user-list.component.html',
  styleUrls: ['./subscribed-user-list.component.css']
})
export class SubscribedUserListComponent implements OnInit {
  displayedColumns: string[] = ['username', 'userID'];
  dataSource: SubscribedUser[];
  constructor(private webService: WebService) { }

  ngOnInit(): void {
    this.getData();
  }
  getData(): void {
    this.webService.getSubscriptionList().subscribe(success => {
      this.dataSource = success.subscribedUsers;
    }, err => {
      alert(err);
    });
  }
  unsubscribed(removeUserID: number): void {
    this.dataSource = this.dataSource.filter(({ userID }) => userID !== removeUserID);
  }

}
