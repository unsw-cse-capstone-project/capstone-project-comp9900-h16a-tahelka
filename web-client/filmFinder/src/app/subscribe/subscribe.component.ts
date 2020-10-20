import {Component, Input, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';

@Component({
  selector: 'app-subscribe',
  templateUrl: './subscribe.component.html',
  styleUrls: ['./subscribe.component.css']
})
export class SubscribeComponent implements OnInit {

  @Input() public userID;
  public subscribed = true;
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  subscribe(): void {
    if (this.subscribed) {
      this.webService.subscribeUser(this.userID).subscribe(success => {
        this.subscribed = success;
        console.log(this.userID, 'User Id subscribed');
      }, err => {
        alert(JSON.stringify(err));
      });
      this.subscribed = false;
    }
    else {
      this.webService.unsubscribeUser(this.userID).subscribe(success => {
        this.subscribed = success;
        console.log(this.userID, 'User Id unsubscribed');
      }, err => {
        alert(JSON.stringify(err));
      });
      this.subscribed = true;
    }
  }
}
