import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';

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
    dob: new FormControl(2020, Validators.required)
  });
  yearList = this.generateYear();
  public generateYear(): object {
    const retVal = [];
    for (let i = 2020; i > 1900; i--) {
      retVal.push({value: i});
    }
    return retVal;
  }
  constructor(private router: Router) { }

  ngOnInit(): void {
  }
  navigate(pathToNavigate: string): void {
    this.router.navigate([pathToNavigate]);
  }
}
