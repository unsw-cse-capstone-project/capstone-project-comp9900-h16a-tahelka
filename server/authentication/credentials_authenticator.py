from db_engine import Session
from authentication.hash_matcher import HashMatcher
from authentication.token_generator import TokenGenerator

from models.User import User

from werkzeug.exceptions import Unauthorized
from flask import g


class CredentialsAuthenticator:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):
        user = self.find_filmfinder()
        if user is None:
            raise Unauthorized

        matcher = HashMatcher(self.password, user.password)
        if not matcher.is_matched():
            raise Unauthorized

        # Put the authenticated user as current user in global
        g.user = user.userID

        return user, TokenGenerator(user).generate()

    def find_filmfinder(self):
        session = Session()
        return session.query(User).filter(User.username == self.username).first()
