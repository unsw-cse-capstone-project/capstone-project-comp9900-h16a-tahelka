import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {SignupComponent} from './signup/signup.component';
import {SearchComponent} from './search/search.component';
import {AuthGuard} from './_helpers/auth.guard';
import {RecommendComponent} from './recommend/recommend.component';
import {BrowseComponent} from './browse/browse.component';

const routes: Routes = [
  {
    path:  'test',
    component:  RecommendComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'browse',
    component: BrowseComponent,
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
