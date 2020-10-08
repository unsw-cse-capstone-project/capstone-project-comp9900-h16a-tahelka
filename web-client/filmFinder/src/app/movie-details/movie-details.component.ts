import {Component, Input, OnInit} from '@angular/core';
import {MovieResult} from '../models/MovieResult';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  @Input() desc: string;
  @Input() movie: MovieResult;
  constructor() { }

  ngOnInit(): void {
    console.log(this.movie);
  }
  movieDetails(): void {
    console.log(this.movie);
  }

}
