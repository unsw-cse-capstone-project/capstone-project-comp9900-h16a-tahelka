import {Component, Input, OnInit} from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {WebService} from '../services/web.service';
import {Search} from '../models/Search';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  @Input() desc: string;
  @Input() movie: MovieResult;
  constructor(private webService: WebService) { }

  ngOnInit(): void {
    console.log(this.movie);
  }
  movieDetails(): void {
      this.webService.movieDetails(this.movie.movieID).subscribe(success => {
        console.log(success);
      }, err => {
        alert(JSON.stringify(err));
      });
    }

}
