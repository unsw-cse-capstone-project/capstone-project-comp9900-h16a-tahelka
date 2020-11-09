from flask import request, g
from flask_restx import Namespace, fields, reqparse, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.BannedList import BannedList
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.Person import Person
from util.IntValidations import is_valid_integer
from util.StringValidations import validate_search_keywords
from util.RatingCalculator import compute
from sqlalchemy import desc


mood_mappings = {'Indifferent': {'Western', 'War', 'Biography', 'Family'},
                 'Sad and Rejected': {'Musical', 'Comedy', 'Romance'},
                 'Flirty': {'Musical', 'Drama', 'Fantasy', 'Romance'},
                 'Energetic and Excited': {'Thriller', 'Musical', 'Crime', 'Drama',
                                           'Fantasy', 'Adventure', 'Sci-Fi', 'Action', 'Comedy'
                                          },
                 'Stressed': {'Animation'},
                 'Weird': {'Film-Noir', 'Crime', 'Drama', 'Horror', 'Mystery'}
                }

api = Namespace('Movies', path = '/movies',
                description='Search for Movies and get Movie details')

film_summary = api.model('Film Summary',
                         {'movieID': fields.Integer,
                          'title': fields.String,
                          'year': fields.Integer,
                          'rating': fields.String(description = 'Average rating out of 5')
                         }
                        )

search_results = api.model('Search Results',
                           {'data': fields.List(fields.Nested(film_summary)),
                            'count': fields.Integer(description = 'The total number of search results')
                           }
                          )

parser = reqparse.RequestParser()
parser.add_argument('page size', 10, type = int)
parser.add_argument('page index', required = True, type = int)
parser.add_argument('name', '')
parser.add_argument('description', '')
parser.add_argument('mood', choices = tuple(mood_mappings.keys()))
parser.add_argument('genre',
                    choices = ('Western', 'Thriller', 'Musical', 'War', 'Film-Noir', 'Crime',
                               'Drama', 'Horror', 'Mystery', 'Fantasy', 'Adventure', 'Sci-Fi',
                               'Animation', 'Biography', 'Action', 'Comedy', 'Family', 'Romance'
                              )
                   )
parser.add_argument('director', '')

@api.route('')
class MovieSearch(Resource):
    @api.response(200, 'Success', search_results)
    @api.response(400,
                  'Page size and page index must both be non-negative integers\n'
                  'Name and description keyword strings, and director, must each be no more than 250 characters long\n'
                 )
    @api.response(401, 'Authentication token is missing')
    @api.expect(parser, validate = True)
    def get(self):
        '''
        Search for movies by name, description, mood, genre or director.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        args = parser.parse_args()
        page_size = args.get('page size')
        is_valid_integer(page_size)
        page_index = args.get('page index')
        is_valid_integer(page_index)
        name_keywords = validate_search_keywords(args.get('name'))
        description_keywords = validate_search_keywords(args.get('description'))
        director = validate_search_keywords(args.get('director'))
        genre = args.get('genre')
        mood = args.get('mood')
        if mood:
            genres = mood_mappings[mood] | {genre} if genre else mood_mappings[mood]
        else:
            genres = {genre} if genre else None
        session = Session()
        query = session.query(Movie.movieID, Movie.title, Movie.year,
                              Movie.ratings_sum, Movie.review_count
                             ).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                      Movie.description.ilike(f'%{description_keywords}%')
                                     ).order_by(desc(Movie.average_rating(g.userID)), Movie.title)
        count = session.query(Movie.movieID).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                                    Movie.description.ilike(f'%{description_keywords}%')
                                                   )
        if director:
            query = query.join(FilmDirector).join(Person).filter(Person.name.ilike(f'%{director}%'))
            count = count.join(FilmDirector).join(Person).filter(Person.name.ilike(f'%{director}%'))
        if genres:
            query = query.join(GenreOfFilm).join(Genres).filter(Genres.genre.in_(genres)).distinct()
            count = count.join(GenreOfFilm).join(Genres).filter(Genres.genre.in_(genres)).distinct()
        banned_users = tuple(banned_user for banned_user, in session.query(BannedList.bannedUserID)
                                                                    .filter(BannedList.userID == g.userID)
                            )
        search_results = [{'movieID': movieID, 'title': title, 'year': year,
                           'rating': str(compute(movieID, g.userID, ratings_sum, review_count, banned_users))
                          } for movieID, title, year, ratings_sum, review_count
                                in query.limit(page_size).offset(page_size * page_index)
                         ]
        return {'data': search_results, 'count': count.count()}, 200
