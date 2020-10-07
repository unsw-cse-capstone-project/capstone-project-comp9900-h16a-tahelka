from db_engine import Session
from flask import request
from flask_restx import Namespace, Resource
from authentication.token_authenticator import TokenAuthenticator
from models.Movie import Movie
from werkzeug.exceptions import NotFound


api = Namespace('Movies', 'Find movies', '/movies')

@api.route('/<int:movieID>')
class MovieDetails(Resource):
    def get(self, movieID):
        '''
        View a movie's full details.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        movie = session.query(Movie).filter(Movie.movieID == movieID).one_or_none()
        if movie is None:
            raise NotFound
        full_details = {}
        return full_details, 200
