from db_engine import Session
from flask import request, g
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from authentication.token_authenticator import TokenExtractor
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Watchlist import Watchlist


api = Namespace('Movie Review', path = '/movies')

movie_review = api.model('Movie Review',
                         {'rating': fields.Float, 'review': fields.String}
                        )

@api.route('/<int:id>/reviews')
class MovieReview(Resource):
    @api.response(201, 'Success')
    @api.expect(movie_review)
    def post(self, id):
        '''
        Leave a movie review
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        movie = session.query(Movie).filter(Movie.movieID == id)
        session.add(Watchlist(id, g.userID))
        session.add(MovieReview(id, g.userID,
                                request.json['rating'], request.json['review']
                               )
                   )
        movie.ratings_sum += request.json['rating']
        movie.review_count += 1
        session.commit()
        return 201
