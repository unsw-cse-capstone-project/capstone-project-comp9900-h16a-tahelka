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
  constructor(private authenticationService: AuthenticationService, private router: Router) { }

  ngOnInit(): void {
  }
  logout(): void {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }
}
