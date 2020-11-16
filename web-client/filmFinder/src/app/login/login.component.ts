import { Component, OnInit } from '@angular/core';
import {FormGroup, FormControl, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import { AuthenticationService } from '../services/authentication.service';
import {WebService} from '../services/web.service';
import {AuthenticatedUser} from '../models/AuthenticatedUser';
import {User} from '../models/User';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', Validators.required)
  });
  user: User;
  constructor(private webService: WebService, private router: Router, private authenticationService: AuthenticationService) { }

  ngOnInit(): void {
  }
  // http call for login
  login(): void {
    this.user = this.loginForm.value;
    this.webService.login(this.user).subscribe(success => {
      const authUser = new AuthenticatedUser(success.username, success.email, success.token, success.userID);
      this.authenticationService.login(authUser);
      this.navigate('/search');
    }, err => {
      // left comment for user who forgets port placement
      alert(JSON.stringify(err));
    });
    this.navigate('/search');
  }
  navigate(pathToNavigate: string): void {
    this.router.navigate([pathToNavigate]);
  }
}
