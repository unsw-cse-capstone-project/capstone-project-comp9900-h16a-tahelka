import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {SignupComponent} from './signup/signup.component';
import {SearchComponent} from './search/search.component';
import {AuthGuard} from './_helpers/auth.guard';
import {BrowseComponent} from './browse/browse.component';
import {WishlistDetailsComponent} from './wishlist-details/wishlist-details.component';
import {SubscribedUserListComponent} from './subscribed-user-list/subscribed-user-list.component';
import {SubscribedWishlistMoviesComponent} from './subscribed-wishlist-movies/subscribed-wishlist-movies.component';
import {WatchedMoviesComponent} from './watched-movies/watched-movies.component';

const routes: Routes = [
  {
    path:  'watched-movies',
    component:  WatchedMoviesComponent,
    canActivate: [AuthGuard]
  },
  {
    path:  'subscribed-wishlist-movies',
    component:  SubscribedWishlistMoviesComponent,
    canActivate: [AuthGuard]
  },
  {
    path:  'subscribed-users',
    component:  SubscribedUserListComponent,
    canActivate: [AuthGuard]
  },
  {
    path:  'wishlist/:id',
    component:  WishlistDetailsComponent,
    canActivate: [AuthGuard]
  },
  {
    path:  'wishlist',
    component:  WishlistDetailsComponent,
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
