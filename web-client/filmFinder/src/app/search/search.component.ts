import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {Search} from '../models/Search';
import {WebService} from '../services/web.service';
import {MovieResult} from '../models/MovieResult';
import {PageChangedModel} from '../models/PageChangedModel';


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
  loading = false;
  searchClicked = false;
  constructor(private webService: WebService) {
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
  search(page= 0, size= 10): void {
    this.loading = true;
    this.searchClicked = true;
    const queryCopy = (JSON.parse(JSON.stringify(this.searchForm.value)));
    this.webService.search(this.clean(queryCopy), page, size).subscribe(success => {
      this.searchResult = success.data;
      this.searchResultLength = success.count;
      this.loading = false;
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
  pageChangedEvent(event: PageChangedModel): void {
    this.loading = true;
    const queryCopy = (JSON.parse(JSON.stringify(this.searchForm.value)));
    this.webService.search(this.clean(queryCopy), event.pageIndex, event.pageSize).subscribe(success => {
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
  resetForm(): void {
    this.searchForm.reset();
  }
}
