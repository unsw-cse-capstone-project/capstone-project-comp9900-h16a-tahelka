from flask import current_app
from flask import g
import jwt
from jwt.exceptions import InvalidTokenError
import time
from werkzeug.exceptions import Forbidden, Unauthorized

from authentication.token_extractor import TokenExtractor

class TokenAuthenticator:
    def __init__(self, auth_header, must_be_admin):
        self.auth_header = auth_header
        self.must_be_admin = must_be_admin

    def authenticate(self):
        # Decode
        payload = self.decode_token()
        TokenAuthenticator.validate_payload(payload)

        # Set the user_id as global
        g.user_id = payload['id']

        # Check role
        if self.must_be_admin and 'is_admin' not in payload:
            raise Forbidden

    def decode_token(self):
        secret = current_app.config['JWT_SECRET']
        try:
            payload = jwt.decode(self.extract_token(), secret,
                                 algorithms='HS256')
        except(InvalidTokenError):  # check expiry is also done here
            raise Unauthorized

        return payload

    def extract_token(self):
        return TokenExtractor(self.auth_header).extract()

    def validate_payload(payload):
        for key in ['id', 'exp']:
            if key not in payload:
                raise Unauthorized
