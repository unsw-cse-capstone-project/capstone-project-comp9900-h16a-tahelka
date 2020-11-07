from flask import request, g
from flask_restx import Namespace, fields, reqparse, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.Person import Person
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

api = Namespace('Movies', path = '/movies',
                description='Search for Movies and get Movie details')

film_summary = api.model('Film Summary',
                         {'movieID': fields.Integer,
                          'title': fields.String,
                          'year': fields.Integer,
                          'rating': fields.String(description = 'Average rating out of 5')
                         }
                        )

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
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
    @api.response(200, 'Success', [film_summary])
    @api.response(400, 'Name and description keyword strings must each be no more than 250 characters long\n'
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
        name_keywords = validate_search_keywords(args.get('name'))
        description_keywords = validate_search_keywords(args.get('description'))
        director = validate_director(args.get('director'))
        genre = args.get('genre')
        mood = args.get('mood')
        genres = mood_mappings[mood] if mood else None
        if genres:
            if genre:
                genres.add(genre)
        elif genre:
            genres = {genre}
        # Commented out limit because browsing movies by director or
        # genre should return all films by that director or of that genre.
        limit = 30  # TODO: change limit later as needed.
        session = Session()
        if director:
            query = session.query(Movie.movieID, Movie.title, Movie.year,
                                  Movie.ratings_sum, Movie.review_count
                                 ).join(GenreOfFilm).join(Genres)\
                                  .join(FilmDirector).join(Person)\
                                  .filter(Genres.genre.in_(genres),
                                          Person.name == director,
                                          Movie.title.ilike(f'%{name_keywords}%'),
                                          Movie.description.ilike(f'%{description_keywords}%')
                                         ).distinct().limit(limit)\
                        if genres\
                        else session.query(Movie.movieID, Movie.title, Movie.year,
                                           Movie.ratings_sum, Movie.review_count
                                          ).join(FilmDirector).join(Person)\
                                           .filter(Person.name == director,
                                                   Movie.title.ilike(f'%{name_keywords}%'),
                                                   Movie.description.ilike(f'%{description_keywords}%')
                                                  ).limit(limit)
        else:
            query = session.query(Movie.movieID, Movie.title, Movie.year,
                                  Movie.ratings_sum, Movie.review_count
                                 ).join(GenreOfFilm).join(Genres)\
                                  .filter(Genres.genre.in_(genres),
                                          Movie.title.ilike(f'%{name_keywords}%'),
                                          Movie.description.ilike(f'%{description_keywords}%')
                                         ).distinct().limit(limit)\
                        if genres\
                        else session.query(Movie.movieID, Movie.title, Movie.year,
                                           Movie.ratings_sum, Movie.review_count
                                          ).filter(Movie.title.ilike(f'%{name_keywords}%'),
                                                   Movie.description.ilike(f'%{description_keywords}%')
                                                  ).limit(limit)
        search_results = [{'movieID': movieID, 'title': title, 'year': year,
                           'rating': compute(movieID, g.userID, ratings_sum, review_count)
                          } for movieID, title, year, ratings_sum, review_count in query
                         ]
        search_results.sort(key = lambda film: (-film['rating'], film['title']))
        for film in search_results:
            film['rating'] = str(film['rating'])
        return search_results, 200
