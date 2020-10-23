from flask import request, g
from flask_restx import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.WishList import Wishlist
from util.IntValidations import is_valid_integer

api = Namespace('Wishlist', path='/wishlists')

@api.route('/<int:movieID>')
class Wishlists_MovieID(Resource):

    @api.response(204, "Movie removed from Wishlist.")
    @api.response(404, "The parameters submitted are not found")
    def delete(self, movieID):
        '''
        Removes said movie from current user's Wishlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        is_valid_integer(movieID)

        affectedRows = session.query(Wishlist).filter(Wishlist.movieID == movieID)\
            .filter(Wishlist.userID == g.userID).delete()
        # When 0, it means either of movieID or userID are not present in database.
        if affectedRows == 0:
            raise NotFound
        else:
            session.commit()

        return 204

