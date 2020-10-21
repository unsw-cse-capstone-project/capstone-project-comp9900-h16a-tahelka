from flask import request, g
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Subscription import Subscription
from models.Movie import Movie
from models.User import User
from models.WishList import Wishlist

api = Namespace('SubscribedWishlistMovies', path='/subscribedWishlistMovies')

@api.route('')
class SubscribedWishlistMovies(Resource):

    def get(self):
        '''
        Get wishlised movies of the users the current user is subscribed to.
        :return:
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        cid = g.userID

        results = session.query(User.username, Movie.title)\
                .select_from(Subscription)\
                .join(Wishlist, Wishlist.userID == Subscription.subscribedUserID, isouter = True)\
                .join(Movie, Movie.movieID == Wishlist.movieID, isouter = True)\
                .join(User, User.userID == Subscription.subscribedUserID)\
                .filter(Subscription.userID == cid)

        movies = list()
        for username, title in results:
            movies.append({'username': username, 'title': title})

        response = {'movies':movies}
        return response, 200