import { Component, OnInit } from '@angular/core';
import {BrowseGenre} from '../models/BrowseGenre';
import {MovieResult} from '../models/MovieResult';
import {FormControl, FormGroup} from '@angular/forms';
import {WebService} from '../services/web.service';
import {Search} from '../models/Search';

@Component({
  selector: 'app-browse-genre',
  templateUrl: './browse-genre.component.html',
  styleUrls: ['./browse-genre.component.css']
})
export class BrowseGenreComponent implements OnInit {
  genre: object[];
  searchResult: MovieResult[];
  genreForm: FormGroup = new FormGroup({
    genre: new FormControl('')
  });
  constructor(private webService: WebService) {
    this.genre = [
      {value: 'Animation'},
      {value: 'Adult'},
      {value: 'Documentary'},
      {value: 'Mystery'},
      {value: 'Fantasy'},
      {value: 'Family'},
      {value: 'Drama'},
      {value: 'Biography'},
      {value: 'Adventure'},
      {value: 'Sci-Fi'},
      {value: 'Comedy'},
      {value: 'Western'},
      {value: 'Action'},
      {value: 'Musical'},
      {value: 'News'},
      {value: 'Sport'},
      {value: 'Horror'},
      {value: 'Romance'},
      {value: 'Reality-TV'},
      {value: 'Music'},
      {value: 'Film-Noir'},
      {value: 'Thriller'},
      {value: 'War'},
      {value: 'History'},
      {value: 'Crime'}
    ];
  }
  ngOnInit(): void {
  }
  search(): void {
    this.webService.search(this.genreForm.value).subscribe(success => {
      this.searchResult = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
