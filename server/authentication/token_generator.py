from flask import current_app
import jwt
import time

class TokenGenerator:
    def __init__(self, filmfinder):
        self.filmfinder = filmfinder

    def generate(self):
        payload = self.construct_payload()
        secret = current_app.config['SECRET_KEY']
        return jwt.encode(payload, secret, algorithm='HS256').decode()

    def construct_payload(self):
        payload = {
            'id': self.filmfinder.userID,
            'username': self.filmfinder.username,
            'email': self.filmfinder.email,
            'exp': TokenGenerator.decide_expire_time()
        }

        return payload

    def decide_expire_time():
        # Expire in 24 hours
        return int(time.time()) + (60 * 60 * 24)
