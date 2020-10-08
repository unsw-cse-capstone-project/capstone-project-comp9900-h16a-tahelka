import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {SignupComponent} from './signup/signup.component';
import {SearchComponent} from './search/search.component';
import {AuthGuard} from './_helpers/auth.guard';
import {TestGroundComponent} from './test-ground/test-ground.component';

const routes: Routes = [
  {
    path:  'test',
    component: TestGroundComponent,
    canActivate: [AuthGuard]
  },
  {
    path:  'search',
    component:  SearchComponent,
    canActivate: [AuthGuard]
  },
  {
    path:  'signup',
    component:  SignupComponent
  },
  {
    path:  '**',
    component:  LoginComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
