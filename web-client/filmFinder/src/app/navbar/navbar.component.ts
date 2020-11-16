import {Component, Input, OnInit} from '@angular/core';
import { Router } from '@angular/router';
import {AuthenticationService} from '../services/authentication.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  @Input() isLoggedIn: boolean;
  username: string;
  constructor(private authenticationService: AuthenticationService, private router: Router) { }
  // get data from auth service
  ngOnInit(): void {
    if (this.authenticationService.currentUserValue){
      this.username = this.authenticationService.currentUserValue.username;
    }
  }
  // clears session storage in auth service
  logout(): void {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
  navigate(pathToNavigate: string): void {
    this.router.navigate([pathToNavigate]);
  }
}
