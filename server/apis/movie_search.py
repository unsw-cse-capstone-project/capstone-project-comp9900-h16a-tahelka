from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.Person import Person
from operator import itemgetter


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
@api.param('description', 'Description keywords')
@api.param('genre')
@api.param('director')
class MovieSearch(Resource):
    @api.response(200, 'Success', [film_summary])
    @api.response(401, 'Authentication token is missing')
    def get(self):
        '''
        Search for movies by name, description, genre or director.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        # Commented out limit because browsing movies by director or
        # genre should return all films by that director or of that genre.
        # limit = 100  # TODO: change limit later as needed.
        name_keywords = ' '.join(word for word in request.args.get('name').strip().split())\
                            if 'name' in request.args\
                            else ''
        description_keywords = ' '.join(word for word in request.args.get('description').strip().split())\
                                   if 'description' in request.args\
                                   else ''
        search_results = Session().query(Movie.movieID, Movie.title, Movie.year,
                                         Movie.ratings_sum, Movie.review_count
                                        ).join(GenreOfFilm).join(Genres)\
                                         .join(FilmDirector).join(Person)\
                                         .filter(Genres.genre == request.args.get('genre'),
                                                 Person.name == request.args.get('director'),
                                                 Movie.title.ilike(f'%{name_keywords}%'),
                                                 Movie.description.ilike(f'%{description_keywords}%')
        #                                       )[: limit]\
                                                )\
            if 'genre' in request.args and 'director' in request.args\
            else Session().query(Movie.movieID, Movie.title, Movie.year,
                                 Movie.ratings_sum, Movie.review_count
                                ).join(GenreOfFilm).join(Genres)\
                                 .filter(Genres.genre == request.args.get('genre'),
                                         Movie.title.ilike(f'%{name_keywords}%'),
                                         Movie.description.ilike(f'%{description_keywords}%')
        #                               )[: limit]\
                                        )\
                     if 'genre' in request.args\
                     else Session().query(Movie.movieID, Movie.title, Movie.year,
                                          Movie.ratings_sum, Movie.review_count
                                         ).join(FilmDirector).join(Person)\
                                          .filter(Person.name == request.args.get('director'),
                                                  Movie.title.ilike(f'%{name_keywords}%'),
                                                  Movie.description.ilike(f'%{description_keywords}%')
        #                                        )[: limit]\
                                                 )\
                              if 'director' in request.args\
                              else Session().query(Movie.movieID, Movie.title, Movie.year,
                                                   Movie.ratings_sum, Movie.review_count
                                                  ).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                                           Movie.description.ilike(f'%{description_keywords}%')
        #                                                 )[: limit]
                                                          )
        search_results = [{'movieID': movieID, 'title': title, 'year': year,
                           'rating': ratings_sum / review_count if review_count else 0
                          } for movieID, title, year, ratings_sum, review_count in search_results
                         ]
        return sorted(sorted(search_results, key = itemgetter('title')),
                      key = itemgetter('rating'), reverse = True
                     ), 200
