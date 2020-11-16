import { Component, OnInit } from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {FormControl, FormGroup} from '@angular/forms';
import {WebService} from '../services/web.service';
import {Search} from '../models/Search';
import {PageChangedModel} from '../models/PageChangedModel';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-browse-director',
  templateUrl: './browse-director.component.html',
  styleUrls: ['./browse-director.component.css']
})
export class BrowseDirectorComponent implements OnInit {
  searchObject: Search;
  searchResult: MovieResult[];
  directorForm: FormGroup = new FormGroup({
    director: new FormControl('')
  });
  loading = false;
  searchResultLength: number;
  searchClicked = false;
  snackBarDuaration = 2000;
  constructor(private webService: WebService, private snackBar: MatSnackBar) { }

  ngOnInit(): void {
  }
  // http call to get data
  search(): void {
    this.searchClicked = true;
    this.searchObject = this.directorForm.value;
    this.webService.search(this.directorForm.value, 0, 10).subscribe(success => {
      this.searchResult = success.data;
      this.searchResultLength = success.count;
      this.loading = false;
    }, err => {
      this.snackBar.open(
        UserMessageConstant.BROWSE_DIRECTOR_ERROR,
        UserMessageConstant.DISMISS,
        { duration: this.snackBarDuaration});
    });
  }
  pageChangedEvent(event: PageChangedModel): void {
    this.loading = true;
    this.webService.search(this.directorForm.value, event.pageIndex, event.pageSize).subscribe(success => {
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
