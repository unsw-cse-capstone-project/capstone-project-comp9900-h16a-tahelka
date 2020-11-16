import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {WebService} from '../services/web.service';
import {SubscribedUser} from '../models/SubscribedUser';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';

@Component({
  selector: 'app-subscribed-user-list',
  templateUrl: './subscribed-user-list.component.html',
  styleUrls: ['./subscribed-user-list.component.css']
})
export class SubscribedUserListComponent implements OnInit, AfterViewInit {
  displayedColumns: string[] = ['username', 'userID'];
  dataSource: SubscribedUser[];
  dataSourceMatTable = new MatTableDataSource<SubscribedUser>();
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  constructor(private webService: WebService) { }

  ngOnInit(): void {
    this.getData();
  }
  ngAfterViewInit(): void {
    this.dataSourceMatTable.sort = this.sort;
  }
  // http call to get data
  getData(): void {
    this.webService.getSubscriptionList().subscribe(success => {
      this.dataSource = success.subscribedUsers;
      this.dataSourceMatTable = new MatTableDataSource<SubscribedUser>(this.dataSource);
      this.dataSourceMatTable.paginator = this.paginator;
      this.dataSourceMatTable.sort = this.sort;
    }, err => {
      alert(err);
    });
  }
  // http call to unsubscribe
  unsubscribed(removeUserID: number): void {
    this.dataSource = this.dataSource.filter(({ userID }) => userID !== removeUserID);
    this.dataSourceMatTable = new MatTableDataSource<SubscribedUser>(this.dataSource);
    this.dataSourceMatTable.paginator = this.paginator;
    this.dataSourceMatTable.sort = this.sort;
  }
  pageChanged(event: any): any {
  }
}
