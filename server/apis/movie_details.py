from flask import request
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.FilmCast import FilmCast
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Person import Person
from models.User import User
from werkzeug.exceptions import NotFound


api = Namespace('Movie Details', path = '/movies')

movie_review = api.model('Movie Review',
                         {'userID': fields.Integer,
                          'username': fields.String(description = 'The FilmFinder that left this review'),
                          'rating': fields.Float(description = 'A rating out of 5'),
                          'review': fields.String(description = "The FilmFinder's review of the movie")
                         }
                        )

movie_recommendation = api.model('Movie Recommendation',
                                 {'movieID': fields.Integer,
                                  'title': fields.String,
                                  'year': fields.Integer
                                 }
                                )

movie_details = api.model('Full Movie Details',
                          {'movieID': fields.Integer,
                           'title': fields.String,
                           'year': fields.Integer,
                           'description': fields.String,
                           'genre': fields.List(fields.String),
                           'director': fields.List(fields.String),
                           'cast': fields.List(fields.String),
                           'rating': fields.Float(description = 'Average rating out of 5'),
                           'reviews': fields.List(fields.Nested(movie_review)),
                           'recommendations': fields.List(fields.Nested(movie_recommendation))
                          }
                         )

@api.route('/<int:id>')
class MovieDetails(Resource):
    @api.response(200, 'Success', movie_details)
    @api.response(401, 'Authentication token is missing')
    @api.response(404, 'Movie was not found')
    @api.doc(params={'id': 'Identifier of movie'})
    def get(self, id):
        '''
        View a movie's full details.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        movie = session.query(Movie.movieID, Movie.title,
                              Movie.year, Movie.description,
                              Movie.ratings_sum, Movie.review_count
                             ).filter(Movie.movieID == id).one_or_none()
        if not movie:
            raise NotFound
        query = session.query(Genres.genre).join(GenreOfFilm)\
                                           .filter(GenreOfFilm.movieID == id)
        genres = [genre for genre, in query]
        query = session.query(Person.name).join(FilmDirector)\
                                          .filter(FilmDirector.movieID == id)
        directors = [director for director, in query]
        query = session.query(Person.name).join(FilmCast)\
                                          .filter(FilmCast.movieID == id)
        cast = [member for member, in query]
        query = session.query(User.userID, User.username,
                              MovieReview.rating, MovieReview.review
                             ).join(MovieReview).filter(MovieReview.movieID == id)
        reviews = [{'userID': userID, 'username': username,
                    'rating': rating, 'review': review
                   } for userID, username, rating, review in query
                  ]
        recommendations = []
        return {'movieID': id, 'title': movie.title,
                'year': movie.year, 'description': movie.description,
                'genre': genres, 'director': directors, 'cast': cast,
                'rating': movie.ratings_sum / movie.review_count
                              if movie.review_count else 0,
                'reviews': reviews, 'recommendations': recommendations
               }, 200
