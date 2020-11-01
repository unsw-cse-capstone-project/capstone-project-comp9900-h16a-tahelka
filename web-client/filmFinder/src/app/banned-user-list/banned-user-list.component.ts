import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {WebService} from '../services/web.service';
import {BannedUser} from '../models/BannedUser';
import {SubscribedUser} from '../models/SubscribedUser';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {MatSnackBar} from '@angular/material/snack-bar';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';

@Component({
  selector: 'app-banned-user-list',
  templateUrl: './banned-user-list.component.html',
  styleUrls: ['./banned-user-list.component.css']
})
export class BannedUserListComponent implements OnInit, AfterViewInit  {
  dataSource: BannedUser[];
  dataSourceMatTable = new MatTableDataSource<BannedUser>();
  displayedColumns: string[] = ['username', 'unblock'];
  snackbarDuration = 2000;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
    this.getData();
  }
  ngAfterViewInit(): void {
    this.dataSourceMatTable.sort = this.sort;
  }
  getData(): void {
    this.webService.getBannedUserList().subscribe(success => {
      this.dataSource = success;
      this.dataSourceMatTable = new MatTableDataSource<BannedUser>(this.dataSource);
      this.dataSourceMatTable.paginator = this.paginator;
      this.dataSourceMatTable.sort = this.sort;
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
  pageChanged(event: any): any {
  }
}
