import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {SignupComponent} from './signup/signup.component';
import {SearchComponent} from './search/search.component';

const routes: Routes = [
  { path:  'search', component:  SearchComponent},
  { path:  'signup', component:  SignupComponent},
  { path:  '**', component:  LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
