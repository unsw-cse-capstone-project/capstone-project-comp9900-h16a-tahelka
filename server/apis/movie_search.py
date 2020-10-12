from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Genres import Genres
from models.GenreOfFilm import GenreOfFilm
from models.Movie import Movie


api = Namespace('Movie Search', path = '/movies')

film_summary = api.model('Film Summary',
                         {'movieID': fields.Integer,
                          'title': fields.String,
                          'year': fields.Integer,
                          'rating': fields.Float(description = 'Average rating out of 5')
                         }
                        )

@api.route('')
@api.param('name', 'Name keywords')
@api.param('genre', 'Genre keywords')
@api.param('description', 'Description keywords')
class MovieSearch(Resource):
    @api.response(200, 'Success', [film_summary])
    def get(self):
        '''
        Search for movies by name.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        limit = 100  # TODO: change limit later as needed.
        name_keywords = request.args.get('name') if 'name' in request.args else ''
        description_keywords\
            = request.args.get('description') if 'description' in request.args else ''
        search_results\
            = Session().query(Movie.movieID, Movie.title, Movie.year,
                              Movie.ratings_sum, Movie.review_count
                             ).join(GenreOfFilm).join(Genres)\
                              .filter(Genres.genre == request.args.get('genre'),
                                      Movie.title.ilike(f'%{name_keywords}%'),
                                      Movie.description.ilike(f'%{description_keywords}%')
                                     )[: limit]\
            if 'genre' in request.args\
            else Session().query(Movie.movieID, Movie.title, Movie.year,
                                 Movie.ratings_sum, Movie.review_count
                                ).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                         Movie.description.ilike(f'%{description_keywords}%')
                                        )[: limit]
        return [{'movieID': movieID, 'title': title, 'year': year,
                 'rating': ratings_sum / review_count if review_count else 0
                } for movieID, title, year, ratings_sum, review_count in search_results
               ], 200
