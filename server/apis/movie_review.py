from flask import request, g
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Watchlist import Watchlist
from werkzeug.exceptions import NotFound
from time import time

api = Namespace('Movie Review', path = '/movies')

film_review = api.model('Movie Review',
                        {'rating': fields.String(description = 'A rating from 0 to 5.'),
                         'review': fields.String
                        }
                       )

@api.route('/<int:id>/reviews')
class FilmReview(Resource):
    @api.response(201, 'Success')
    @api.response(404, 'Movie was not found')
    @api.expect(film_review)
    def post(self, id):
        '''
        Leave a movie review
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        movie = session.query(Movie).filter(Movie.movieID == id).one_or_none()
        if movie is None:
            raise NotFound
        query = session.query(Watchlist).filter(Watchlist.movieID == id,
                                                Watchlist.userID == g.userID
                                               ).one_or_none()
        if query is None:
            session.add(Watchlist(id, g.userID))
        query = session.query(MovieReview).filter(MovieReview.movieID == id,
                                                  MovieReview.userID == g.userID
                                                 ).one_or_none()
        rating = float(request.json['rating'])
        if query is None:  # FilmFinder has not reviewed this movie before.
            session.add(MovieReview(id, g.userID, rating,
                                    request.json['review'], time()
                                   )
                       )
            movie.ratings_sum += rating
            movie.review_count += 1
            session.commit()
            return {'message': 'Review received.'}, 201
        #FilmFinder is updating a previously left review.
        movie.ratings_sum += rating - query.rating
        query.rating = rating
        query.review = request.json['review']
        query.timestamp = time()
        session.commit()
        return {'message': 'Review updated.'}, 201
