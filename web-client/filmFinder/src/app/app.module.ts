import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule} from '@angular/forms';

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
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
