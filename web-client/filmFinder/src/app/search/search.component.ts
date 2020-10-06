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
      {value: 'action'},
      {value: 'comedy'}
    ];
    this.mood = [
      {value: 'happy'},
      {value: 'sad'},
    ];
  }

  ngOnInit(): void {
  }

}
