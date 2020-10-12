import { Component, OnInit } from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {FormControl, FormGroup} from '@angular/forms';
import {WebService} from '../services/web.service';
import {BrowseDirector} from '../models/BrowseDirector';

@Component({
  selector: 'app-browse-director',
  templateUrl: './browse-director.component.html',
  styleUrls: ['./browse-director.component.css']
})
export class BrowseDirectorComponent implements OnInit {
  browseDirectorObject: BrowseDirector;
  searchResult: MovieResult[];
  directorForm: FormGroup = new FormGroup({
    director: new FormControl('')
  });
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  search(): void {
    this.browseDirectorObject = new BrowseDirector(this.directorForm.value.director);
    this.webService.browseDirector(this.browseDirectorObject).subscribe(success => {
      this.searchResult = success;
    }, err => {
      alert(JSON.stringify(err));
    });
  }
}
