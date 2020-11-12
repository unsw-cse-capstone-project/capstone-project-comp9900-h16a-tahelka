from flask import request, g
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Movie import Movie
from models.User import User
from models.WishList import Wishlist
from models.Subscription import Subscription

from util.IntValidations import is_valid_integer
from util.RatingCalculator import compute

api = Namespace('Wishlist', path='/wishlists')

film_summary = api.model('Film Summary',
                         {'movieID': fields.Integer,
                          'title': fields.String,
                          'year': fields.Integer,
                          'rating': fields.String(description = 'Average rating out of 5')
                         }
                        )

resp_model = api.model('Response',
                       {'username':fields.String,
                        'wishlist': fields.List(fields.Nested(film_summary)),
                        'isSubscribed': fields.Boolean})

@api.route('/<int:userID>')
class Wishlists_UserID(Resource):

    @api.response(200, "Movies in user's Wishlist", resp_model)
    @api.response(404, "User not found")
    @api.doc(params={'userID': 'Identifier of user'})
    def get(self, userID):
        '''
        View said user's Wishlist of movies.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        is_valid_integer(userID)


        results = session.query(Movie.movieID, Movie.title, Movie.year, Movie.ratings_sum, \
                                Movie.review_count).filter(Wishlist.userID == userID)\
            .filter(Wishlist.movieID == Movie.movieID)

        username = session.query(User.username).filter(User.userID == userID).first()

        if not username:
            raise NotFound

        movies = list()
        for movieID, title, year, ratings_sum, review_count in results:
            movies.append({'movieID': movieID, 'title': title, 'year': year,
                           'rating': str(compute(movieID, g.userID, ratings_sum, review_count))
                           })

        # Check if current user is subscribed to said user
        res = session.query(Subscription).filter(Subscription.userID == g.userID) \
            .filter(Subscription.subscribedUserID == userID).first()
        session.close()

        isSubscribed = False
        if res:
            isSubscribed = True

        response = {'username': username, 'wishlist': movies, 'isSubscribed': isSubscribed}
        return response, 200
