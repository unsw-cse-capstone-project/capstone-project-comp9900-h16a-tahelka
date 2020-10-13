from flask import request, g
from flask_restx import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.WishList import Wishlist


api = Namespace('Wishlist', path='/wishlists')

@api.route('/<int:movieID>')
class Wishlists_byId(Resource):

    @api.response(201, "Movie removed from Wishlist.")
    @api.response(400, "The parameters submitted are invalid.")
    def delete(self, movieID):
        '''
        Removes said movie from user's Wishlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        try:
            wishlistItem = session.query(Wishlist).filter(Wishlist.movieID == movieID)\
                .filter(Wishlist.userID == g.userID).delete()
            session.commit()
        except: #TODO: handle missing item from database.
            print('Error')
            pass

        response = {'message': 'Movie removed from Wishlist.'}
        return response, 200


