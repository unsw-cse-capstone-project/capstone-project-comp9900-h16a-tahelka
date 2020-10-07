export class AuthenticatedUser {
  username: string;
  email: string;
  token: string;
  constructor(username: string, email: string, token: string) {
    this.username = username;
    this.token = token;
    this.email = email;
  }
}
