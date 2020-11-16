import {Component, DoCheck, EventEmitter, Input, OnChanges, OnInit, Output, QueryList, ViewChild, ViewChildren} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {MovieDetailsComponent} from '../movie-details/movie-details.component';
import {MovieResult} from '../models/MovieResult';
import {Recommendations} from '../models/Recommendations';
import {ReviewListComponent} from '../review-list/review-list.component';
import {WishlistRemove} from '../models/WishlistRemove';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import { SimpleChanges } from '@angular/core';

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
export class SearchResultComponent implements OnInit, OnChanges  {
  columnsToDisplay = ['title', 'year', 'rating'];
  @Input() dataSource: MovieResult[];
  @Input() dataSourceLength: number;
  dataSourceMatTable = new MatTableDataSource<MovieResult>();
  expandedElement: MovieResult | null;
  @ViewChildren(MovieDetailsComponent) movieDetailsComponents: QueryList<MovieDetailsComponent>;
  @ViewChildren(ReviewListComponent) movieReviewListComponents: QueryList<ReviewListComponent>;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @Input() loading: boolean;
  @Output() pageChangedEvent = new EventEmitter<any>();
  constructor() { }

  ngOnInit(): void {
  }
  getMovieDetailsInChildComponent(movie: MovieResult): void {
    // Get data onclick
    this.movieDetailsComponents.forEach(component => {
      if (component.movie.movieID === movie.movieID) {
        component.movieDetails();
      }
    });
  }
  tabChanged(event: any): void {
  }
  // add reviews
  setReviewList(event: any, movie: MovieResult): void {
    this.movieReviewListComponents.forEach(component => {
      if (component.movieID === movie.movieID) {
        component.setMovieReviews(event);
      }
    });
  }
  // when wishlist is removed update datasource
  wishlistMovieRemoved(wishlistRemoved: WishlistRemove, movie: MovieResult): void {
    this.dataSource = this.dataSource.filter(obj => obj !== movie);
    this.dataSourceMatTable = new MatTableDataSource<MovieResult>(this.dataSource);
    this.dataSourceMatTable._updateChangeSubscription();
    this.dataSourceMatTable.paginator = this.paginator;
  }
  // when watchlist is removed update datasource
  watchlistMovieRemoved(movieID: number, movie: MovieResult): void {
    this.dataSource = this.dataSource.filter(obj => obj !== movie);
    this.dataSourceMatTable = new MatTableDataSource<MovieResult>(this.dataSource);
    this.dataSourceMatTable._updateChangeSubscription();
    this.dataSourceMatTable.paginator = this.paginator;
  }
  // to capitalize table headers
  capitalize(s: string): string
  {
    return s && s[0].toUpperCase() + s.slice(1);
  }
  pageChanged(event: any): void {
    if (event.pageIndex > event.previousPageIndex) {
      this.pageChangedEvent.emit(event);
    }
  }
  // lifecycle hooks
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.dataSource && !changes.dataSource.firstChange) {
      if (changes.dataSourceLength) {
        changes.dataSource.currentValue.length = changes.dataSourceLength.currentValue;
      }
      this.dataSourceMatTable = new MatTableDataSource<MovieResult>(changes.dataSource.currentValue);
      this.dataSourceMatTable._updateChangeSubscription();
      this.dataSourceMatTable.paginator = this.paginator;
    } else {
      if (this.dataSource) {
        this.dataSource.length = this.dataSourceLength;
      }
      this.dataSourceMatTable = new MatTableDataSource<MovieResult>(this.dataSource);
      this.dataSourceMatTable._updateChangeSubscription();
      this.dataSourceMatTable.paginator = this.paginator;
    }
  }
}
