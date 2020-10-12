import {Component, Input, OnInit, QueryList, ViewChild, ViewChildren} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {MovieDetailsComponent} from '../movie-details/movie-details.component';
import {MovieResult} from '../models/MovieResult';
import {Recommendations} from '../models/Recommendations';
import {ReviewListComponent} from '../review-list/review-list.component';
export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
  description: string;
}
@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class SearchResultComponent implements OnInit {
  columnsToDisplay = ['title', 'year', 'rating'];
  @Input() dataSource: MovieResult[];
  expandedElement: MovieResult | null;
  @Input() movieSearchResult: MovieResult[];
  @ViewChildren(MovieDetailsComponent) movieDetailsComponents: QueryList<MovieDetailsComponent>;
  @ViewChildren(ReviewListComponent) movieReviewListComponents: QueryList<ReviewListComponent>;
  recommendations: Recommendations[];
  constructor() { }

  ngOnInit(): void {
  }
  getMovieDetailsInChildComponent(movie: MovieResult): void {
    // Try to find a better way here
    this.movieDetailsComponents.forEach(component => {
      if (component.movie.movieID === movie.movieID) {
        component.movieDetails();
      }
    });
  }
  setRecommendations(recommendations: Recommendations[]): void {
    this.recommendations = recommendations;
  }
  tabChanged(event: any): void {
  }
  setReviewList(event: any): void {
    this.movieReviewListComponents.forEach(component => {
      if (component.movieID === this.expandedElement.movieID) {
        component.setMovieReviews(event);
      }
    });
  }
}
