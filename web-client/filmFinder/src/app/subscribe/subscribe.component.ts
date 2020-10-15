import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-subscribe',
  templateUrl: './subscribe.component.html',
  styleUrls: ['./subscribe.component.css']
})
export class SubscribeComponent implements OnInit {

  subscribed = true;
  constructor() { }

  ngOnInit(): void {
  }
  subscribe(): void {
    if (this.subscribed) {
      this.subscribed = false;
    }
    else {
      this.subscribed = true;
    }
  }
}
