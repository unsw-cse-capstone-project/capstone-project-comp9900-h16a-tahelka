from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Movie import Movie
from models.User import User
from models.Watchlist import Watchlist
from util.IntValidations import is_valid_integer

api = Namespace('Watchlist', path='/watchlists')

@api.route('/<int:userID>')
class Wishlists_UserID(Resource):

    @api.response(200, "Movies in user's Watchlist.")
    @api.response(404, "User not found")
    @api.doc(params={'userID': 'Identifier of user'})
    def get(self, userID):
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        is_valid_integer(userID)

        limit = 10
        results = session.query(Movie.movieID, Movie.title, Movie.year, Movie.ratings_sum, \
                                Movie.review_count).filter(Watchlist.userID == userID)\
            .filter(Watchlist.movieID == Movie.movieID).limit(limit)

        username = session.query(User.username).filter(User.userID == userID).first()

        if not username:
            raise NotFound

        movies = list()
        for movieID, title, year, ratings_sum, review_count in results:
            movies.append({'movieID': movieID, 'title': title, 'year': year,
                           'rating': ratings_sum / review_count if review_count else 0
                           })


        response = {'username': username, 'watchlist': movies}
        return response, 200
