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
  searchResultLength: number;
  searchForm: FormGroup = new FormGroup({
    name: new FormControl(),
    description: new FormControl(),
    genre: new FormControl(),
    mood: new FormControl()
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
  search(offset= 0, limit= 15): void {
    const queryCopy = (JSON.parse(JSON.stringify(this.searchForm.value)));
    this.webService.search(this.clean(queryCopy), offset, limit).subscribe(success => {
      this.searchResult = success.data;
      this.searchResultLength = success.count;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
  clean(obj: any): any {
    for (const propName in obj) {
      if (obj[propName] === null || obj[propName] === undefined || obj[propName] === '') {
        delete obj[propName];
      }
    }
    return obj;
  }
  pageChangedEvent(event: any): void {
    this.search(10, 5);
  }
}
