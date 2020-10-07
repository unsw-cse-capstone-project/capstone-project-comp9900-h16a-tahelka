import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {NewUser} from '../models/NewUser';
import {WebService} from '../services/web.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  signUpForm: FormGroup = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
    confirmPassword: new FormControl('', Validators.required),
    yob: new FormControl(2020, Validators.required)
  });
  yearList = this.generateYear();
  newUser: NewUser;
  public generateYear(): object {
    const retVal = [];
    for (let i = 2020; i > 1900; i--) {
      retVal.push({value: i});
    }
    return retVal;
  }
  constructor(private router: Router, private webService: WebService) { }

  ngOnInit(): void {
  }
  signup(): void {
    if (this.signUpForm.value.confirmPassword === this.signUpForm.value.password) {
      this.newUser = this.signUpForm.value;
      this.webService.signup(this.newUser).subscribe(success => {
          console.log(success);
        },
        err => {
          alert(err);
        });
    } else {
      alert('password and confirm password do not match');
    }
  }
  navigate(pathToNavigate: string): void {
    this.router.navigate([pathToNavigate]);
  }
}
