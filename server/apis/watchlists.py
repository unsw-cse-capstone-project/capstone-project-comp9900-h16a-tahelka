from flask import request, g
from flask_restx import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Watchlist import Watchlist

from util.IntValidations import is_valid_integer

api = Namespace('Watchlist', path='/watchlists',
                description='Operations on Watchlist.')

watchlist_model = api.model('Watchlist', {
    'movieID': fields.Integer(description='Identifier of movie'),
})

@api.route('')
class Watchlists(Resource):

    @api.expect(watchlist_model)
    @api.response(201, "Movie added to Watchlist.")
    @api.response(400, "The parameters submitted are invalid.")
    def post(self):
        '''
            Adds a movie to the users' Watchlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        movieID = request.json.get('movieID')

        is_valid_integer(movieID)

        new_watchlist = Watchlist(movieID, g.userID)
        session = Session()
        session.add(new_watchlist)
        try:
            session.commit()
        except IntegrityError:  #If Watchlist already present
            session.rollback()
            raise BadRequest

        response = {'message':'Movie added to Watchlist.'}
        return response, 201


