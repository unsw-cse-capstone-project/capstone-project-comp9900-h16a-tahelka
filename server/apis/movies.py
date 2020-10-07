from db_engine import Session
from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from models.Movie import Movie
from models.User import User
from werkzeug.exceptions import NotFound
from string import punctuation


api = Namespace('Movies', 'Find movies', '/movies')

# def transform(s):
#     return set(s.lower().translate(str.maketrans('', '', punctuation)).split())

@api.route('')
@api.param('name', 'Name search keywords')
class MovieSearch(Resource):
    def get(self):
        '''
        Search for movies by name.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        name_keywords = request.args.get('name') if 'name' in request.args else ''
        matches = Session().query(Movie.movieID, Movie.title,
                                  Movie.year, Movie.avg_rating
                                 ).filter(Movie.title.ilike(f"%{name_keywords}%"))
        return [{'movieID': movieID, 'title': title,
                 'year': year, 'rating': avg_rating
                } for movieID, title, year, avg_rating in matches
               ], 200

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
