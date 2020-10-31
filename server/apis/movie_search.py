from flask import request, g
from flask_restx import Namespace, fields, reqparse, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.Person import Person
from util.IntValidations import is_valid_integer
from util.StringValidations import validate_search_keywords, validate_director
from util.RatingCalculator import compute


mood_mappings = {'Indifferent': {'Western', 'War', 'Biography', 'Family'},
                 'Sad and Rejected': {'Musical', 'Comedy', 'Romance'},
                 'Flirty': {'Musical', 'Drama', 'Fantasy', 'Romance'},
                 'Energetic and Excited': {'Thriller', 'Musical', 'Crime', 'Drama',
                                           'Fantasy', 'Adventure', 'Sci-Fi', 'Action', 'Comedy'
                                          },
                 'Stressed': {'Animation'},
                 'Weird': {'Film-Noir', 'Crime', 'Drama', 'Horror', 'Mystery'}
                }

api = Namespace('Movies', path = '/movies')

film_summary = api.model('Film Summary',
                         {'movieID': fields.Integer,
                          'title': fields.String,
                          'year': fields.Integer,
                          'rating': fields.String(description = 'Average rating out of 5')
                         }
                        )

search_results = api.model('Search Results',
                           {'search_results': fields.List(fields.Nested(film_summary)),
                            'count': fields.Integer(description = 'The total number of search results')
                           }
                          )

parser = reqparse.RequestParser()
parser.add_argument('offset', required = True, type = int)
parser.add_argument('limit', required = True, type = int)
parser.add_argument('name', '')
parser.add_argument('description', '')
parser.add_argument('mood', choices = tuple(mood_mappings.keys()))
parser.add_argument('genre',
                    choices = ('Western', 'Thriller', 'Musical', 'War', 'Film-Noir', 'Crime',
                               'Drama', 'Horror', 'Mystery', 'Fantasy', 'Adventure', 'Sci-Fi',
                               'Animation', 'Biography', 'Action', 'Comedy', 'Family', 'Romance'
                              )
                   )
parser.add_argument('director')

@api.route('')
class MovieSearch(Resource):
    @api.response(200, 'Success', search_results)
    @api.response(400, 'Offset and limit must both be non-negative integers\n'
                       'Name and description keyword strings must each be no more than 250 characters long\n'
                       'Director must match the name of a director'
                 )
    @api.response(401, 'Authentication token is missing')
    @api.expect(parser, validate = True)
    def get(self):
        '''
        Search for movies by name, description, mood, genre or director.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        args = parser.parse_args()
        offset = args.get('offset')
        is_valid_integer(offset)
        limit = args.get('limit')
        is_valid_integer(limit)
        name_keywords = validate_search_keywords(args.get('name'))
        description_keywords = validate_search_keywords(args.get('description'))
        director = validate_director(args.get('director'))
        genre = args.get('genre')
        mood = args.get('mood')
        if mood:
            genres = mood_mappings[mood] | {genre} if genre else mood_mappings[mood]
        else:
            genres = {genre} if genre else None
        session = Session()
        if director:
            if genres:
                query = session.query(Movie.movieID, Movie.title, Movie.year,
                                      Movie.ratings_sum, Movie.review_count
                                     ).join(GenreOfFilm).join(Genres)\
                                      .join(FilmDirector).join(Person)\
                                      .filter(Genres.genre.in_(genres),
                                              Person.name == director,
                                              Movie.title.ilike(f'%{name_keywords}%'),
                                              Movie.description.ilike(f'%{description_keywords}%')
                                             ).distinct().offset(offset).limit(limit)
                count = session.query(Movie.movieID).join(GenreOfFilm).join(Genres)\
                                                    .join(FilmDirector).join(Person)\
                                                    .filter(Genres.genre.in_(genres),
                                                            Person.name == director,
                                                            Movie.title.ilike(f'%{name_keywords}%'),
                                                            Movie.description.ilike(f'%{description_keywords}%')
                                                           ).distinct().count()
            else:
                query = session.query(Movie.movieID, Movie.title, Movie.year,
                                      Movie.ratings_sum, Movie.review_count
                                     ).join(FilmDirector).join(Person)\
                                      .filter(Person.name == director,
                                              Movie.title.ilike(f'%{name_keywords}%'),
                                              Movie.description.ilike(f'%{description_keywords}%')
                                             ).offset(offset).limit(limit)
                count = session.query(Movie.movieID).join(FilmDirector).join(Person)\
                                                    .filter(Person.name == director,
                                                            Movie.title.ilike(f'%{name_keywords}%'),
                                                            Movie.description.ilike(f'%{description_keywords}%')
                                                           ).count()
        else:
            if genres:
                query = session.query(Movie.movieID, Movie.title, Movie.year,
                                      Movie.ratings_sum, Movie.review_count
                                     ).join(GenreOfFilm).join(Genres)\
                                      .filter(Genres.genre.in_(genres),
                                              Movie.title.ilike(f'%{name_keywords}%'),
                                              Movie.description.ilike(f'%{description_keywords}%')
                                             ).distinct().offset(offset).limit(limit)
                count = session.query(Movie.movieID).join(GenreOfFilm).join(Genres)\
                                                    .filter(Genres.genre.in_(genres),
                                                            Movie.title.ilike(f'%{name_keywords}%'),
                                                            Movie.description.ilike(f'%{description_keywords}%')
                                                           ).distinct().count()
            else:
                query = session.query(Movie.movieID, Movie.title, Movie.year,
                                      Movie.ratings_sum, Movie.review_count
                                     ).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                              Movie.description.ilike(f'%{description_keywords}%')
                                             ).offset(offset).limit(limit)
                count = session.query(Movie.movieID).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                                            Movie.description.ilike(f'%{description_keywords}%')
                                                           ).count()
        search_results = [{'movieID': movieID, 'title': title, 'year': year,
                           'rating': compute(movieID, g.userID, ratings_sum, review_count)
                          } for movieID, title, year, ratings_sum, review_count in query
                         ]
        search_results.sort(key = lambda film: (-film['rating'], film['title']))
        for film in search_results:
            film['rating'] = str(film['rating'])
        return {'search_results': search_results, 'count': count}, 200
