import { Component, Input, OnInit } from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {WebService} from '../services/web.service';
import {MovieDetails} from '../models/MovieDetails';
import {Recommend} from '../models/Recommend';

@Component({
  selector: 'app-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.css']
})
export class RecommendComponent implements OnInit {

  @Input() movie: MovieResult;
  dataSource: MovieDetails[];
  movieDetailsObject: MovieDetails;
  recommendSource: Recommend[];
  columnsToDisplay: string[] = ['title', 'year'];
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  recommend(): void{
    this.webService.recommend(this.movie.movieID).subscribe(success => {
      this.movieDetailsObject = success;
      this.dataSource = [success];
    }, err => {
      alert(JSON.stringify(err));
    });
    this.recommendSource = this.movieDetailsObject.recommendations;
  }
}

