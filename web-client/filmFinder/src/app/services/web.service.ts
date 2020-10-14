import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {AuthenticationService} from './authentication.service';
import {Observable} from 'rxjs';
import { User } from '../models/User';
import { NewUser } from '../models/NewUser';
import {Search} from '../models/Search';
import {Review} from '../models/Review';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class WebService {
  API_URL =  'http://127.0.0.1:5000/api/v1/';
  constructor(private http: HttpClient, private authenticationService: AuthenticationService) { }
  login(user: User): Observable<any> {
    const loginUrl = this.API_URL + 'tokens';
    return this.http.post(loginUrl, user, httpOptions);
  }
  signup(user: NewUser): Observable<any> {
    const signupUrl = this.API_URL + 'users';
    return this.http.post(signupUrl, user, httpOptions);
  }
  search(searchObject: any): Observable<any> {
    const moviesUrl = this.API_URL + 'movies';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    // const params = new HttpParams()
    //   .set('name', searchObject.name);
    return this.http.get(moviesUrl, {params: searchObject, headers});
  }
  movieDetails(id: number): Observable<any> {
    const moviesUrl = this.API_URL + 'movies/' + id.toString();
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(moviesUrl, {headers});
  }
  review(review: Review, movieId: number): Observable<any> {
    const reviewUrl = this.API_URL + 'movies/' + movieId.toString() + '/reviews';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.post(reviewUrl, review, {headers});
  }
  // TODO: Remove this as we can get data from movie details but we will need this to get user-defined recommendations
  // recommend(id: number): Observable<any>{
  //   const moviesUrl = this.API_URL + 'movies/' + id.toString();
  //   let headers = new HttpHeaders();
  //   headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
  //   return this.http.get(moviesUrl, {headers});
  // }
  wishlistAdd(movieId: number): Observable<any> {
    const wishlistUrl =  this.API_URL + 'wishlists';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    const body = {
      movieID: movieId
    };
    return this.http.post(wishlistUrl, body, {headers});
  }
  wishlistRemove(movieId: number): Observable<any> {
    const wishlistUrl =  this.API_URL + 'wishlists/' + movieId.toString();
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.delete(wishlistUrl, {headers});
  }
  watchlist(movieId: number): Observable<any> {
    const watchlistUrl = this.API_URL + 'watchlists';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    const body = {
      movieID: movieId
    };
    return this.http.post(watchlistUrl, body, {headers});
  }
  browseDirector(browseDirectorObject: any): Observable<any>{
    const moviesUrl = this.API_URL + 'movies';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(moviesUrl, {params: browseDirectorObject, headers});
  }
  browseGenre(browseGenreObject: any): Observable<any>{
    const moviesUrl = this.API_URL + 'movies';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(moviesUrl, {params: browseGenreObject, headers});
  }
  wishListDetails(id: number): Observable<any>{
    let moviesUrl = this.API_URL + 'wishlists/';
    if (id !== -1) {
      moviesUrl = moviesUrl + id.toString();
    }
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(moviesUrl, {headers});
  }
}
