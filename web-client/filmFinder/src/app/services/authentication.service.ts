import { Injectable } from '@angular/core';
import { AuthenticatedUser } from '../models/AuthenticatedUser';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private currentUser: AuthenticatedUser;
  constructor() {
    this.currentUser = JSON.parse(sessionStorage.getItem('currentUser'));
  }
  public get currentUserValue(): AuthenticatedUser {
    return JSON.parse(sessionStorage.getItem('currentUser'));
  }
  login(authenticatedUser: AuthenticatedUser): void {
    sessionStorage.setItem('currentUser', JSON.stringify(authenticatedUser));
  }
  logout(): void {
    sessionStorage.removeItem('currentUser');
  }
}
