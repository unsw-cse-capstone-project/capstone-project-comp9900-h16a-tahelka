import { Component, OnInit } from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {FormControl, FormGroup} from '@angular/forms';
import {WebService} from '../services/web.service';
import {BrowseDirector} from '../models/BrowseDirector';
import {Search} from '../models/Search';

@Component({
  selector: 'app-browse-director',
  templateUrl: './browse-director.component.html',
  styleUrls: ['./browse-director.component.css']
})
export class BrowseDirectorComponent implements OnInit {
  searchObject: Search;
  browseDirectorObject: BrowseDirector;
  searchResult: MovieResult[];
  directorForm: FormGroup = new FormGroup({
    director: new FormControl('')
  });
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  search(): void {
    this.searchObject = this.directorForm.value;
    this.webService.search(this.searchObject).subscribe(success => {
      this.searchResult = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
