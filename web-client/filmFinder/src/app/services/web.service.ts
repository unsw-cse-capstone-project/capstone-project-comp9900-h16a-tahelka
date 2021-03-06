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
  search(searchObject: any, page: number, size: number): Observable<any> {
    const moviesUrl = this.API_URL + 'movies';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    searchObject.page_index = page;
    searchObject.page_size = size;
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
  recommend(id: number, useDirector = 1, useGenre= 1): Observable<any>{
    const moviesUrl = this.API_URL + 'movies/' + id.toString() + '/recommendations';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    let params = new HttpParams().append('use_director', useDirector.toString());
    params = params.append('use_genre', useGenre.toString());
    return this.http.get(moviesUrl, {headers, params});
  }
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
  getWatchlist(): Observable<any> {
    const watchlistUrl = this.API_URL + 'watchlists';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(watchlistUrl, {headers});
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
  removeWatchlist(movieId: number): Observable<any> {
    const watchlistUrl = this.API_URL + `watchlists/${movieId}`;
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.delete(watchlistUrl,  {headers});
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
  unsubscribeUser(userId: number): Observable<any> {
    const subscribeUrl =  this.API_URL + 'subscribeUsers/' + userId.toString();
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.delete(subscribeUrl,  {headers});
  }
  subscribeUser(userId: number): Observable<any> {
    const subscribeUrl =  this.API_URL + 'subscribeUsers';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    const body = {
      userID: userId
    };
    return this.http.post(subscribeUrl, body, {headers});
  }
  getSubscriptionList(): Observable<any>{
    const moviesUrl = this.API_URL + 'subscribeUsers';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(moviesUrl, {headers});
  }
  wishlistImport(userId: number): Observable<any> {
    const subscribeUrl =  this.API_URL + `wishlists/${userId}/import`;
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.post(subscribeUrl, {}, {headers});
  }
  getSubscribedWishlistMovies(): Observable<any>{
    const moviesUrl = this.API_URL + 'subscribedWishlistMovies';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(moviesUrl, {headers});
  }
  blockUser(userID: number): Observable<any> {
    const subscribeUrl =  this.API_URL + 'bannedlists';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.post(subscribeUrl, {userID}, {headers});
  }
  getBannedUserList(): Observable<any>{
    const moviesUrl = this.API_URL + 'bannedlists';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.get(moviesUrl, {headers});
  }
  unBannedUser(userID: number): Observable<any>{
    const moviesUrl = this.API_URL + `bannedlists/${userID}`;
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    return this.http.delete(moviesUrl, {headers});
  }
}
