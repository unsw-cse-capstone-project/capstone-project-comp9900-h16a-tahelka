from flask import request, g
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.BannedList import BannedList
from models.FilmCast import FilmCast
from models.FilmDirector import FilmDirector
from models.GenreOfFilm import GenreOfFilm
from models.Genres import Genres
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Person import Person
from models.User import User
from werkzeug.exceptions import NotFound
from util.IntValidations import is_valid_integer
from util.RatingCalculator import compute


api = Namespace('Movies', path = '/movies')

movie_review = api.model('Movie Review',
                         {'userID': fields.Integer,
                          'username': fields.String(description = 'The FilmFinder that left this review'),
                          'rating': fields.String(description = 'A rating out of 5'),
                          'review': fields.String(description = "The FilmFinder's review of the movie")
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
                           'rating': fields.String(description = 'Average rating out of 5'),
                           'reviews': fields.List(fields.Nested(movie_review))
                          }
                         )

@api.route('/<int:id>')
@api.param('id', 'The Movie identifier')
class MovieDetails(Resource):
    @api.response(200, 'Success', movie_details)
    @api.response(400, 'id must be a non-negative integer')
    @api.response(401, 'Authentication token is missing')
    @api.response(404, 'Movie was not found')
    def get(self, id):
        '''
        View a movie's full details.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        is_valid_integer(id)
        session = Session()
        movie = session.query(Movie.movieID, Movie.title,
                              Movie.year, Movie.description,
                              Movie.ratings_sum, Movie.review_count
                             ).filter(Movie.movieID == id).one_or_none()
        if not movie:
            raise NotFound
        genres = [genre for genre, in session.query(Genres.genre).join(GenreOfFilm)
                                                                 .filter(GenreOfFilm.movieID == id)
                 ]
        directors = [director for director, in session.query(Person.name)
                                                      .join(FilmDirector)
                                                      .filter(FilmDirector.movieID == id)
                    ]
        cast = [member for member, in session.query(Person.name).join(FilmCast)
                                                                .filter(FilmCast.movieID == id)
               ]
        reviews = session.query(User.userID, User.username,
                                MovieReview.rating, MovieReview.review
                               ).join(MovieReview)\
                                .filter(MovieReview.movieID == id,
                                        User.userID.notin_(session.query(BannedList.bannedUserID)
                                                                  .filter(BannedList.userID == g.userID)
                                                          )
                                       )
        reviews = [{'userID': userID, 'username': username,
                    'rating': str(rating), 'review': review
                   } for userID, username, rating, review in reviews
                  ]
        recommendations = [{'movieID': 57012,
                            'title': 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb',
                            'year': 1964
                           },
                           {'movieID': 62622, 'title': '2001: A Space Odyssey', 'year': 1968},
                           {'movieID': 66921, 'title': 'A Clockwork Orange', 'year': 1971}
                          ]
        return {'movieID': id, 'title': movie.title,
                'year': movie.year, 'description': movie.description,
                'genre': genres, 'director': directors, 'cast': cast,
                'rating': str(compute(id, g.userID, movie.ratings_sum, movie.review_count)),
                'reviews': reviews, 'recommendations': recommendations
               }, 200
