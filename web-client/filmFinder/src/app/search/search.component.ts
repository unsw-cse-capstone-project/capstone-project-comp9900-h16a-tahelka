import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  genre: object[];
  mood: object[];
  searchForm: FormGroup = new FormGroup({
    movieName: new FormControl(''),
    movieDescription: new FormControl(''),
    movieGenre: new FormControl(''),
    mood: new FormControl('')
  });
  constructor() {
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

}
