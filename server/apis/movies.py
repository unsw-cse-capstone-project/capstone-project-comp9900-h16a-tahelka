from db_engine import Session
from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from models.Movie import Movie
from string import punctuation


api = Namespace('Search', path = '/movies', description = 'Search for movies')

def remove_punctuation(s):
    return s.translate(str.maketrans('', '', punctuation))

def matches(keywords, value):
    return set(remove_punctuation(keywords.lower()).split())\
           <= set(remove_punctuation(value.lower()).split())

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
        name = request.args.get('name')
        return [{'movieID': movieID, 'title': title,
                 'year': year, 'rating': avg_rating
                } for movieID, title, year, avg_rating
                      in Session().query(Movie.movieID, Movie.title,
                                         Movie.year, Movie.avg_rating
                                        )
                      if matches(name, title)
               ], 200
