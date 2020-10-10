from flask import request, g
from flask_restx import Namespace, fields, Resource

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Movie import Movie
from models.MovieReview import MovieReview as mrModel
from models.Watchlist import Watchlist

api = Namespace('Movie Review', path = '/movies')

movie_review_model = api.model('Movie Review',
                               {'rating': fields.Float, 'review': fields.String}
                               )

@api.route('/<int:id>/reviews')
class MovieReview(Resource):
    @api.response(201, 'Success')
    @api.expect(movie_review_model)
    def post(self, id):
        '''
        Leave a movie review
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        movie = session.query(Movie).filter(Movie.movieID == id).first()
        watchlist = Watchlist(id, g.userID)

        rating = request.json['rating']
        review = request.json['review']
        movieReview = mrModel(id, g.userID, rating, review)

        session.add(watchlist)
        session.add(movieReview)

        movie.ratings_sum += request.json['rating']
        movie.review_count += 1
        session.commit()
        return 201
