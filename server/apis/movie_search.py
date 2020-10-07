from db_engine import Session
from flask import request
from flask_restx import Namespace, Resource
from authentication.token_authenticator import TokenAuthenticator
from models.Movie import Movie


api = Namespace('Movie Search', path = '/movies')

@api.route('')
@api.param('name', 'Name search keywords')
class MovieSearch(Resource):
    def get(self):
        '''
        Search for movies by name.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        name_keywords = request.args.get('name') if 'name' in request.args else ''
        search_results = Session().query(Movie.movieID, Movie.title,
                                         Movie.year, Movie.avg_rating
                                        ).filter(Movie.title.ilike(f'%{name_keywords}%'))
        return [{'movieID': movieID, 'title': title,
                 'year': year, 'rating': avg_rating
                } for movieID, title, year, avg_rating in search_results
               ], 200
