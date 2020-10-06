from flask import current_app
from flask import g
import jwt
from jwt.exceptions import InvalidTokenError
import time
from werkzeug.exceptions import Forbidden, Unauthorized

from tahelka.auth.token_extractor import TokenExtractor

class TokenAuthenticator:
    def __init__(self, auth_header):
        self.auth_header = auth_header

    def authenticate(self):
        # Decode
        payload = self.decode_token()
        TokenAuthenticator.validate_payload(payload)

        # Set the user_id as global
        g.user_id = payload['id']

    def decode_token(self):
        secret = current_app.config['SECRET_KEY']
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
