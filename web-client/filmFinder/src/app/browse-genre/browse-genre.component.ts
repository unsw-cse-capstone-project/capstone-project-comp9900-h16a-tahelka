import { Component, OnInit } from '@angular/core';
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
  showBrowse: false;
  searchResult: MovieResult[];
  genreForm: FormGroup = new FormGroup({
    genre: new FormControl('')
  });
  constructor(private webService: WebService) {
    this.genre = [
      {value: 'Action'},
      {value: 'Thriller'},
      {value: 'Romance'},
      {value: 'Sci-Fi'},
      {value: 'War'},
      {value: 'Drama'},
      {value: 'Mystery'},
      {value: 'Crime'},
      {value: 'Horror'},
      {value: 'Musical'},
      {value: 'Western'},
      {value: 'Sport'},
      {value: 'Music'},
      {value: 'History'},
      {value: 'Family'},
      {value: 'Animation'},
      {value: 'Biography'},
      {value: 'Comedy'},
      {value: 'Adventure'},
      {value: 'Fantasy'},
      {value: 'Film-Noir'}
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
