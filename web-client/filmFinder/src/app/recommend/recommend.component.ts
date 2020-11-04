import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {WebService} from '../services/web.service';
import {MovieDetails} from '../models/MovieDetails';
import {Recommendations} from '../models/Recommendations';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import {BannedUser} from '../models/BannedUser';

@Component({
  selector: 'app-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.css']
})
export class RecommendComponent implements OnInit {

  @Input() recommendSource: Recommendations[];
  dataSourceMatTable = new MatTableDataSource<Recommendations>();
  columnsToDisplay: string[] = ['title', 'year'];
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  // TODO: Remove this as we will get recommendation from parent as input
  // recommend(): void{
  //   this.webService.recommend(this.movie.movieID).subscribe(success => {
  //     this.movieDetailsObject = success;
  //     this.dataSource = [success];
//        this.dataSourceMatTable = new MatTableDataSource<Recommendations>(this.recommendSource);
  //      this.dataSourceMatTable.paginator = this.paginator;
  //      this.dataSourceMatTable.sort = this.sort;
  //   }, err => {
  //     alert(JSON.stringify(err));
  //   });
  //   this.recommendSource = this.movieDetailsObject.recommendations;
  // }
}

