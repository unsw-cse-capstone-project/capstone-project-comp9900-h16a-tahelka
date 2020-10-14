import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Search} from '../models/Search';
import {AuthenticatedUser} from '../models/AuthenticatedUser';
import {WebService} from '../services/web.service';
import {MovieResult} from '../models/MovieResult';


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  genre: object[];
  mood: object[];
  searchObject: Search;
  searchResult: MovieResult[];
  searchForm: FormGroup = new FormGroup({
    name: new FormControl(''),
    description: new FormControl(''),
    genre: new FormControl(''),
    mood: new FormControl('')
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
    this.mood = [
      {value: 'Indifferent'},
      {value: 'Sad and Rejected'},
      {value: 'Flirty'},
      {value: 'Energetic and Excited'},
      {value: 'Stressed'},
      {value: 'Weird'}
    ];
  }

  ngOnInit(): void {
  }
  search(): void {
    // this.searchObject = this.searchForm.value;
    this.webService.search(this.searchForm.value).subscribe(success => {
      this.searchResult = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
