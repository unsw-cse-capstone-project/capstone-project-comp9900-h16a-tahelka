export class AuthenticatedUser {
  username: string;
  email: string;
  token: string;
  userID: number;
  constructor(username: string, email: string, token: string, userID: number) {
    this.username = username;
    this.token = token;
    this.email = email;
    this.userID = userID;
  }
}
