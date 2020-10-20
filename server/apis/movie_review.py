from flask import request, g
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Watchlist import Watchlist
from werkzeug.exceptions import Forbidden, NotFound
from util.IntValidations import is_valid_integer
from util.StringValidations import validate_rating, validate_review


api = Namespace('Movie Review', path = '/movies')

film_review = api.model('Movie Review',
                        {'rating': fields.String(description = 'A rating from 0 to 5.'),
                         'review': fields.String
                        }
                       )

@api.route('/<int:id>/reviews')
class FilmReview(Resource):
    @api.response(201, 'Success')
    @api.response(400,
                  'id must be a non-negative integer\n'
                  'A rating must be in the range from 0 to 5, be a multiple of 0.5, and be no more than 3 characters long\n'
                  'A review has a character limit of 1,000'
                 )
    @api.response(401, 'Authentication token is missing')
    @api.response(403, 'This user has already reviewed this movie')
    @api.response(404, 'Movie was not found')
    @api.expect(film_review)
    def post(self, id):
        '''
        Leave a movie review
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        is_valid_integer(id)
        validate_rating(request.json['rating'])
        validate_review(request.json['review'])
        session = Session()
        movie = session.query(Movie).filter(Movie.movieID == id).one_or_none()
        if not movie:
            raise NotFound
        query = session.query(MovieReview).filter(MovieReview.movieID == id,
                                                  MovieReview.userID == g.userID
                                                 ).one_or_none()
        if query:
            raise Forbidden
        query = session.query(Watchlist).filter(Watchlist.movieID == id,
                                                Watchlist.userID == g.userID
                                               ).one_or_none()
        if not query:
            session.add(Watchlist(id, g.userID))
        request.json['rating'] = float(request.json['rating'])
        session.add(MovieReview(id, g.userID,
                                request.json['rating'], request.json['review']
                               )
                   )
        movie.ratings_sum += request.json['rating']
        movie.review_count += 1
        session.commit()
        return {'message': 'Review saved.'}, 201
