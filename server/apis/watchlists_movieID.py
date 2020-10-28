from flask import request, g
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Watchlist import Watchlist

from util.IntValidations import is_valid_integer


api = Namespace('Watchlist', path='/watchlists')

@api.route('/<int:movieID>')
class Watchlists_MovieID(Resource):

    @api.response(204, "Movie removed from Watchlist.")
    @api.response(404, "The parameters submitted are not found")
    @api.doc(params={'movieID': 'Identifier of movie'})
    def delete(self, movieID):
        '''
        Removes said movie from current user's Watchlist.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        is_valid_integer(movieID)

        affectedRows = session.query(Watchlist).filter(Watchlist.movieID == movieID)\
            .filter(Watchlist.userID == g.userID).delete()
        # When 0, it means either of movieID or userID are not present in database.
        if affectedRows == 0:
            raise NotFound
        else:
            session.commit()

        return 204

