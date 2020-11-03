from flask import request, g
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.User import User
from models.WishList import Wishlist
from util.IntValidations import is_valid_integer

api = Namespace('WishlistImport', path='/wishlists',
                description='Import Wishlist of said user')

@api.route('/<int:userID>/import')
class Wishlists_UserID(Resource):

    @api.doc(params={'userID': 'Identifier of user'})
    @api.response(201, "Wishlisted Movies imported")
    @api.response(200, "No Movies were imported")
    @api.response(404, "User not found")
    def post(self, userID):
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        is_valid_integer(userID)

        # User not Found
        if not session.query(User).filter(User.userID == userID).first():
            raise NotFound

        cID = g.userID
        new = set(session.query(Wishlist.movieID).filter(Wishlist.userID == userID))
        cur = set(session.query(Wishlist.movieID).filter(Wishlist.userID == cID))

        # Add only absent movies
        toAdd = new.difference(cur)
        if toAdd:
            for movie in toAdd:
                for m in movie:
                    wl = Wishlist(m, cID)
                session.add(wl)

            session.commit()
            session.close()
            response = {'message': 'Wishlisted Movies imported'}
            return response, 201

        else:
            response = {'message': 'No Movies were imported'}
            return response, 200