import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MaterialModule} from './material/material.module';
import { LoginComponent } from './login/login.component';
import { NavbarComponent } from './navbar/navbar.component';
import { SignupComponent } from './signup/signup.component';
import { SearchComponent } from './search/search.component';
import {HttpClientModule} from '@angular/common/http';
import { SearchResultComponent } from './search-result/search-result.component';
import { MovieDetailsComponent } from './movie-details/movie-details.component';
import { ReviewComponent } from './review/review.component';
import { RecommendComponent } from './recommend/recommend.component';
import { WishListComponent } from './wish-list/wish-list.component';
import { WatchListComponent } from './watch-list/watch-list.component';
import { ReviewListComponent } from './review-list/review-list.component';
import { BrowseDirectorComponent } from './browse-director/browse-director.component';
import { BrowseComponent } from './browse/browse.component';
import { BrowseGenreComponent } from './browse-genre/browse-genre.component';
import { WishlistDetailsComponent } from './wishlist-details/wishlist-details.component';
import { SubscribeComponent } from './subscribe/subscribe.component';
import { SubscribedUserListComponent } from './subscribed-user-list/subscribed-user-list.component';
import { UnsubscribeComponent } from './unsubscribe/unsubscribe.component';
import { IntegrateWishlistComponent } from './integrate-wishlist/integrate-wishlist.component';
import { SubscribedWishlistMoviesComponent } from './subscribed-wishlist-movies/subscribed-wishlist-movies.component';
import { RemoveMovieWatchlistComponent } from './remove-movie-watchlist/remove-movie-watchlist.component';
import { WatchedMoviesComponent } from './watched-movies/watched-movies.component';
import { BannedUserListComponent } from './banned-user-list/banned-user-list.component';
import {MatSortModule} from '@angular/material/sort';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    NavbarComponent,
    SignupComponent,
    SearchComponent,
    SearchResultComponent,
    MovieDetailsComponent,
    ReviewComponent,
    RecommendComponent,
    WishListComponent,
    WatchListComponent,
    ReviewListComponent,
    BrowseDirectorComponent,
    BrowseComponent,
    BrowseGenreComponent,
    WishlistDetailsComponent,
    SubscribeComponent,
    SubscribedUserListComponent,
    UnsubscribeComponent,
    IntegrateWishlistComponent,
    SubscribedWishlistMoviesComponent,
    RemoveMovieWatchlistComponent,
    WatchedMoviesComponent,
    BannedUserListComponent,
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        MaterialModule,
        ReactiveFormsModule,
        HttpClientModule,
        MatSortModule,
        FormsModule,
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
