import { Component, Input, OnInit } from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {WebService} from '../services/web.service';

@Component({
  selector: 'app-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.css']
})
export class RecommendComponent implements OnInit {

  @Input() movie: MovieResult;
  dataSource: MovieResult[];
  columnsToDisplay: string[] = ['title', 'year'];
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  recommend(): void{
    this.webService.recommend(this.movie.movieID).subscribe(success => {
      this.dataSource = [success];
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}

