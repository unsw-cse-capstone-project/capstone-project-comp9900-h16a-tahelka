from flask import request, g
from flask_restx import Namespace, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.BannedList import Bannedlist
from werkzeug.exceptions import NotFound
from util.IntValidations import is_valid_integer


api = Namespace('Banned List', path = '/bannedlists')

@api.route('/<int:id>')
@api.param('id', 'The User identifier')
class BannedList(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'userID must be a non-negative integer')
    @api.response(401, 'Authentication token is missing')
    @api.response(404, 'Reviewer was not found in Banned List')
    def delete(self, id):
        '''
        Remove a FilmFinder from your Banned List.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        is_valid_integer(id)
        session = Session()
        if not session.query(Bannedlist).filter(Bannedlist.userID == g.userID,
                                                Bannedlist.bannedUserID == id
                                               ).delete():
            session.commit()
            raise NotFound
        session.commit()
        return {'message': 'Reviewer unbanned.'}, 200
