from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.Person import Person


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
    @api.response(401, 'Authentication token is missing')
    def get(self):
        '''
        Search for movies by name, description, mood, genre or director.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        # Commented out limit because browsing movies by director or
        # genre should return all films by that director or of that genre.
        # limit = 100  # TODO: change limit later as needed.
        moods = {'Indifferent': {'Western', 'War', 'Biography', 'Family'},
                 'Sad and Rejected': {'Musical', 'Comedy', 'Romance'},
                 'Flirty': {'Musical', 'Drama', 'Fantasy', 'Romance'},
                 'Energetic and Excited': {'Thriller', 'Musical', 'Crime', 'Drama',
                                           'Fantasy', 'Adventure', 'Sci-Fi', 'Action', 'Comedy'
                                          },
                 'Stressed': {'Animation'},
                 'Weird': {'Film-Noir', 'Crime', 'Drama', 'Horror', 'Mystery'}
                }
        genres = {request.args.get('genre')} & moods[request.args.get('mood')]\
                     if 'genre' in request.args and 'mood' in request.args\
                     else {request.args.get('genre')}\
                              if 'genre' in request.args\
                              else moods[request.args.get('mood')]\
                                       if 'mood' in request.args\
                                       else None
        name_keywords = ' '.join(word for word in request.args.get('name').split())\
                            if 'name' in request.args\
                            else ''
        description_keywords = ' '.join(word for word in request.args.get('description').split())\
                                   if 'description' in request.args\
                                   else ''
        if 'director' in request.args:
            director = ' '.join(word for word in request.args.get('director').split())
            search_results = Session().query(Movie.movieID, Movie.title, Movie.year,
                                             Movie.ratings_sum, Movie.review_count
                                            ).join(GenreOfFilm).join(Genres)\
                                             .join(FilmDirector).join(Person)\
                                             .filter(Genres.genre.in_(genres),
                                                     Person.name.ilike(director),
                                                     Movie.title.ilike(f'%{name_keywords}%'),
                                                     Movie.description.ilike(f'%{description_keywords}%')
        #                                           ).distinct().limit(limit)\
                                                    ).distinct()\
                                 if genres\
                                 else Session().query(Movie.movieID, Movie.title, Movie.year,
                                                      Movie.ratings_sum, Movie.review_count
                                                     ).join(FilmDirector).join(Person)\
                                                      .filter(Person.name.ilike(director),
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
