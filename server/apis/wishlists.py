from db_engine import Session
from flask import Blueprint, request, g
from flask_restx import Namespace, fields, Resource
from authentication.hash_generator import HashGenerator
from authentication.token_authenticator import TokenAuthenticator
from models.WishList import Wishlist
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError

api = Namespace('Wishlist', path='/wishlists',
                description='CRUD movies in Wishlist.')

wishlist_model = api.model('Wishlist', {
    'movieID': fields.Integer(description='Identifier of movie'),
})

@api.route('')
class Wishlists(Resource):
    
    @api.expect(wishlist_model)
    @api.response(201, "Movie added to Wishlist.")
    @api.response(400, "The parameters submitted are invalid.")
    def post(self):
        '''
            Adds a movie to the users' wishlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        movieID = request.json.get('movieID')

        new_wishlist = Wishlist(movieID, g.userID)
        session = Session()
        session.add(new_wishlist)
        try:
            session.commit()
        except IntegrityError:  #If wishlist already present
            session.rollback()
            raise BadRequest

        response = {'message':'Movie added to Wishlist.'}
        return response, 201

