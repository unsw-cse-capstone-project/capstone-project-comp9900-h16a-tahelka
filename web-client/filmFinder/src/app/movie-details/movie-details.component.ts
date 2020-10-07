import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  @Input() desc: string;
  // desc: string;
  constructor() { }

  ngOnInit(): void {
    console.log('init');
  }
  test(de: string): void {
    console.log('test');
    this.desc = de;
  }

}
