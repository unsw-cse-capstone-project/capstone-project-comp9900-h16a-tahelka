import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {WebService} from '../services/web.service';
import {Recommendations} from '../models/Recommendations';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';

@Component({
  selector: 'app-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.css']
})
export class RecommendComponent implements OnInit {

  @Input() movieID: number;
  dataSourceMatTable = new MatTableDataSource<Recommendations>();
  columnsToDisplay: string[] = ['title', 'year'];
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  dataSource: Recommendations[];
  useDirector = true;
  useGenre = true;
  constructor(private webService: WebService) { }
  ngOnInit(): void {
    this.recommend();
  }
  recommend(): void {
    this.webService.recommend(this.movieID, +this.useDirector, +this.useGenre).subscribe(success => {
      this.dataSource = success.movies;
      this.dataSourceMatTable = new MatTableDataSource<Recommendations>(this.dataSource);
      this.dataSourceMatTable.paginator = this.paginator;
      this.dataSourceMatTable.sort = this.sort;
    }, err => {
      console.log(err);
    });
  }
  updatedDirector(event: any): any {
    this.useDirector = ! this.useDirector;
    this.recommend();
  }
  updatedGenre(event: any): any {
    this.useGenre = ! this.useGenre;
    this.recommend();
  }
}

