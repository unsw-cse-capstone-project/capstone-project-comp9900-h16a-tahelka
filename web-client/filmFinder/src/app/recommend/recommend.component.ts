import { Component, Input, OnInit } from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {WebService} from '../services/web.service';
import {MovieDetails} from '../models/MovieDetails';
import {Recommendations} from '../models/Recommendations';

@Component({
  selector: 'app-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.css']
})
export class RecommendComponent implements OnInit {

  @Input() recommendSource: Recommendations[];
  columnsToDisplay: string[] = ['title', 'year'];
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  // TODO: Remove this as we will get recommendation from parent as input
  // recommend(): void{
  //   this.webService.recommend(this.movie.movieID).subscribe(success => {
  //     this.movieDetailsObject = success;
  //     this.dataSource = [success];
  //   }, err => {
  //     alert(JSON.stringify(err));
  //   });
  //   this.recommendSource = this.movieDetailsObject.recommendations;
  // }
}

