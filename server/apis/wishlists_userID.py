from flask import request, g
from flask_restx import Namespace, Resource
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

@api.route('/<int:userID>')
class Wishlists_UserID(Resource):

    @api.response(200, "Movies in user's Wishlist.")
    @api.response(404, "User not found")
    @api.doc(params={'userID': 'Identifier of user'})
    def get(self, userID):
        '''
        View said user's Wishlist of movies.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        is_valid_integer(userID)

        limit = 10
        results = session.query(Movie.movieID, Movie.title, Movie.year, Movie.ratings_sum, \
                                Movie.review_count).filter(Wishlist.userID == userID)\
            .filter(Wishlist.movieID == Movie.movieID).limit(limit)

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
