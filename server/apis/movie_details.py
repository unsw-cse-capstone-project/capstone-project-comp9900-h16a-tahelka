from db_engine import Session
from flask import request
from flask_restx import Namespace, Resource
from authentication.token_authenticator import TokenAuthenticator
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

@api.route('/<int:movieID>')
class MovieDetails(Resource):
    def get(self, movieID):
        '''
        View a movie's full details.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        movie = session.query(Movie.movieID, Movie.title, Movie.year,
                              Movie.description, Movie.avg_rating
                             ).filter(Movie.movieID == movieID).one_or_none()
        if movie is None:
            raise NotFound
        genres = session.query(Genres.genre).filter(GenreOfFilm.movieID
                                                    == movie.movieID
                                                   ).join(GenreOfFilm).all()
        directors = session.query(Person.name).filter(FilmDirector.movieID
                                                      == movie.movieID
                                                     ).join(FilmDirector).all()
        cast = session.query(Person.name).filter(FilmCast.movieID
                                                 == movie.movieID
                                                ).join(FilmCast).all()
        reviews = session.query(User.userID, User.username,
                                MovieReview.rating, MovieReview.review
                               ).filter(MovieReview.movieID == movie.movieID)
        reviews = [{'userID': userID, 'username': username,
                    'rating': rating, 'review': review
                   } for userID, username, rating, review in reviews
                  ]
        recommendations = []
        return {'title': movie.title, 'year': movie.year,
                'description': movie.description, 'genre': genres,
                'director': directors, 'cast': cast, 'rating': movie.avg_rating,
                'reviews': reviews, 'recommendations': recommendations
               }, 200
