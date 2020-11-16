import { Component, OnInit } from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {FormControl, FormGroup} from '@angular/forms';
import {WebService} from '../services/web.service';
import {Search} from '../models/Search';
import {MatSnackBar} from '@angular/material/snack-bar';
import { UserMessageConstant } from '../constants/UserMessageConstant';
import {PageChangedModel} from '../models/PageChangedModel';

@Component({
  selector: 'app-browse-genre',
  templateUrl: './browse-genre.component.html',
  styleUrls: ['./browse-genre.component.css']
})
export class BrowseGenreComponent implements OnInit {
  genre: object[];
  showBrowse: false;
  snackBarDuaration: 3000;
  searchResult: MovieResult[];
  genreForm: FormGroup = new FormGroup({
    genre: new FormControl('')
  });
  loading = false;
  searchResultLength: number;
  searchClicked = false;
  constructor(private webService: WebService, private snackBar: MatSnackBar) {
    this.genre = [
      {value: 'Western'},
      {value: 'Thriller'},
      {value: 'Musical'},
      {value: 'War'},
      {value: 'Film-Noir'},
      {value: 'Crime'},
      {value: 'Drama'},
      {value: 'Horror'},
      {value: 'Mystery'},
      {value: 'Fantasy'},
      {value: 'Adventure'},
      {value: 'Sci-Fi'},
      {value: 'Animation'},
      {value: 'Biography'},
      {value: 'Action'},
      {value: 'Comedy'},
      {value: 'Family'},
      {value: 'Romance'}
    ];
  }
  ngOnInit(): void {
  }
  // http call to get data
  search(): void {
    this.searchClicked = true;
    this.loading = true;
    this.webService.search(this.genreForm.value, 0, 10).subscribe(success => {
      this.searchResult = success.data;
      this.searchResultLength = success.count;
      this.loading = false;
    }, err => {
      this.snackBar.open(
        UserMessageConstant.BROWSE_GENRE_ERROR,
        UserMessageConstant.DISMISS,
        { duration: this.snackBarDuaration});
    });
  }
  // event for page change
  pageChangedEvent(event: PageChangedModel): void {
    this.loading = true;
    this.webService.search(this.genreForm.value, event.pageIndex, event.pageSize).subscribe(success => {
      // set length to actual length
      this.searchResult.length = event.pageSize * event.pageIndex;
      // add data in
      this.searchResult.push(...success.data);
      // set max length in again
      this.searchResultLength = success.count;
      this.loading = false;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
