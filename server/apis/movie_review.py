from flask import request, g
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Movie import Movie
from models.MovieReview import MovieReview
from models.Watchlist import Watchlist
from werkzeug.exceptions import Forbidden, NotFound

api = Namespace('Movie Review', path = '/movies')

film_review = api.model('Movie Review',
                        {'rating': fields.String(description = 'A rating from 0 to 5.'),
                         'review': fields.String
                        }
                       )

@api.route('/<int:id>/reviews')
class FilmReview(Resource):
    @api.response(201, 'Success')
    @api.response(403, 'This user has already reviewed this movie')
    @api.response(404, 'Movie was not found')
    @api.expect(film_review)
    def post(self, id):
        '''
        Leave a movie review
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()
        movie = session.query(Movie).filter(Movie.movieID == id).one_or_none()
        if not movie:
            raise NotFound
        query = session.query(Watchlist).filter(Watchlist.movieID == id,
                                                Watchlist.userID == g.userID
                                               ).one_or_none()
        if not query:
            session.add(Watchlist(id, g.userID))
        query = session.query(MovieReview).filter(MovieReview.movieID == id,
                                                  MovieReview.userID == g.userID
                                                 ).one_or_none()
        if query:
            raise Forbidden
        print('Hello World!')
        request.json['rating'] = float(request.json['rating'])
        session.add(MovieReview(id, g.userID,
                                request.json['rating'], request.json['review']
                               )
                   )
        movie.ratings_sum += request.json['rating']
        movie.review_count += 1
        session.commit()
        return {'message': 'Review saved.'}, 201
