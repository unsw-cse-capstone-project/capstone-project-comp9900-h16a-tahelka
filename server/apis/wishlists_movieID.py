from flask import request, g
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.WishList import Wishlist

api = Namespace('Wishlist', path='/wishlists')

@api.route('/<int:movieID>')
class Wishlists_MovieID(Resource):

    @api.response(204, "Movie removed from Wishlist.")
    @api.response(404, "The parameters submitted are not found")
    @api.doc(params={'movieID': 'Identifier of movie'})
    def delete(self, movieID):
        '''
        Removes said movie from current user's Wishlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        affectedRows = session.query(Wishlist).filter(Wishlist.movieID == movieID)\
            .filter(Wishlist.userID == g.userID).delete()
        # When 0, it means either of movieID or userID are not present in database.
        if affectedRows == 0:
            raise NotFound
        else:
            session.commit()

        return 204

