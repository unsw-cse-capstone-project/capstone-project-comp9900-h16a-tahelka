from db_engine import Session
from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from models.Movie import Movie
from string import punctuation


api = Namespace('Search', path = '/movies', description = 'Search for movies')

def transform(s):
    return set(s.lower().translate(str.maketrans('', '', punctuation)).split())

@api.route('')
class Movies(Resource):
    @api.param('name', description = 'Name search keywords')
    def get(self):
        '''
        Search for movies by name.
        '''
        TokenAuthenticator(request.headers.get('Authorization'),
                           False
                          ).authenticate()
        name_keywords = transform(request.args.get('name'))
        movies = Session().query(Movie.movieID, Movie.title,
                                 Movie.year, Movie.avg_rating
                                )
        search_results = [{'movieID': movieID, 'title': title,
                           'year': year, 'rating': avg_rating
                          } for movieID, title, year, avg_rating in movies
                                if name_keywords <= transform(title)
                         ]
        return search_results, 200
