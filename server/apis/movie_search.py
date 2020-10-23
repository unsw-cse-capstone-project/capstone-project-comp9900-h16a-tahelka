from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.Person import Person
from util.StringValidations import validate_search_keywords, validate_director, validate_genre, validate_mood


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
@api.param('mood')
@api.param('genre')
@api.param('director')
class MovieSearch(Resource):
    @api.response(200, 'Success', [film_summary])
    @api.response(400, 'Name and description keyword strings must each be no more than 250 characters long\n'
                       "Genre must be one of the following: 'Western', 'Thriller', 'Musical', 'War',"
                       "                                    'Film-Noir', 'Crime', 'Drama', 'Horror', 'Mystery',"
                       "                                    'Fantasy', 'Adventure', 'Sci-Fi', 'Animation',"
                       "                                    'Biography', 'Action', 'Comedy', 'Family', 'Romance'\n"
                       "Mood must be one of the following: 'Indifferent', 'Sad and Rejected', 'Flirty',"
                       "                                   'Energetic and Excited', 'Stressed', 'Weird'\n"
                       'Director must match the name of a director'
                 )
    @api.response(401, 'Authentication token is missing')
    def get(self):
        '''
        Search for movies by name, description, mood, genre or director.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        name_keywords = validate_search_keywords(request.args.get('name'))
        description_keywords = validate_search_keywords(request.args.get('description'))
        director = validate_director(request.args.get('director'))
        genre = validate_genre(request.args.get('genre'))
        genres = validate_mood(request.args.get('mood'))
        if genres:
            if genre:
                genres.add(genre)
        elif genre:
            genres = {genre}
        # Commented out limit because browsing movies by director or
        # genre should return all films by that director or of that genre.
        # limit = 100  # TODO: change limit later as needed.
        if director:
            search_results = Session().query(Movie.movieID, Movie.title, Movie.year,
                                             Movie.ratings_sum, Movie.review_count
                                            ).join(GenreOfFilm).join(Genres)\
                                             .join(FilmDirector).join(Person)\
                                             .filter(Genres.genre.in_(genres),
                                                     Person.name == director,
                                                     Movie.title.ilike(f'%{name_keywords}%'),
                                                     Movie.description.ilike(f'%{description_keywords}%')
        #                                           ).distinct().limit(limit)\
                                                    ).distinct()\
                                 if genres\
                                 else Session().query(Movie.movieID, Movie.title, Movie.year,
                                                      Movie.ratings_sum, Movie.review_count
                                                     ).join(FilmDirector).join(Person)\
                                                      .filter(Person.name == director,
                                                              Movie.title.ilike(f'%{name_keywords}%'),
                                                              Movie.description.ilike(f'%{description_keywords}%')
        #                                                    ).limit(limit)
                                                             )
        else:
            search_results = Session().query(Movie.movieID, Movie.title, Movie.year,
                                             Movie.ratings_sum, Movie.review_count
                                            ).join(GenreOfFilm).join(Genres)\
                                             .filter(Genres.genre.in_(genres),
                                                     Movie.title.ilike(f'%{name_keywords}%'),
                                                     Movie.description.ilike(f'%{description_keywords}%')
        #                                           ).distinct().limit(limit)\
                                                    ).distinct()\
                                 if genres\
                                 else Session().query(Movie.movieID, Movie.title, Movie.year,
                                                      Movie.ratings_sum, Movie.review_count
                                                     ).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                                              Movie.description.ilike(f'%{description_keywords}%')
        #                                                    ).limit(limit)
                                                             )
        search_results = [{'movieID': movieID, 'title': title, 'year': year,
                           'rating': round(ratings_sum / review_count, 1) if review_count else 0.0
                          } for movieID, title, year, ratings_sum, review_count in search_results
                         ]
        search_results.sort(key = lambda film: (-film['rating'], film['title']))
        return search_results, 200
