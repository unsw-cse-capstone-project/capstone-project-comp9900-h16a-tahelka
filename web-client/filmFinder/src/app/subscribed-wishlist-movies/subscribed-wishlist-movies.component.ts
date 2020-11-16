import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import { SubscribedWishlistMoviesResult } from '../models/SubscribedWishlistMoviesResult';
import {WebService} from '../services/web.service';
import {MatTableDataSource} from '@angular/material/table';
import {SubscribedUser} from '../models/SubscribedUser';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';

@Component({
  selector: 'app-subscribed-wishlist-movies',
  templateUrl: './subscribed-wishlist-movies.component.html',
  styleUrls: ['./subscribed-wishlist-movies.component.css']
})
export class SubscribedWishlistMoviesComponent implements OnInit, AfterViewInit  {
  displayedColumns: string[] = ['username', 'title'];
  dataSource: SubscribedWishlistMoviesResult[];
  dataSourceMatTable = new MatTableDataSource<SubscribedWishlistMoviesResult>();
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
    this.webService.getSubscribedWishlistMovies().subscribe(success => {
      this.dataSource = success.movies;
      this.dataSourceMatTable = new MatTableDataSource<SubscribedWishlistMoviesResult>(this.dataSource);
      this.dataSourceMatTable.paginator = this.paginator;
      this.dataSourceMatTable.sort = this.sort;
    }, err => {
      alert(err);
    });
  }
  pageChanged(event: any): any {
  }
}
