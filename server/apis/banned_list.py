from flask import request, g
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.BannedList import Bannedlist
from models.User import User
from werkzeug.exceptions import Forbidden, NotFound
from util.IntValidations import is_valid_integer


api = Namespace('Banned List', path = '/bannedlists')

banned_user = api.model('Banned Reviewer', {'userID': fields.Integer})

@api.route('')
class BannedList(Resource):
    @api.response(200, 'Success')
    @api.response(401, 'Authentication token is missing')
    def get(self):
        '''
        View your Banned List.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        banned_list = Session().query(User.userID, User.username)\
                               .join(Bannedlist, User.userID == Bannedlist.bannedUserID)\
                               .filter(Bannedlist.userID == g.userID)
        return [{'userID': userID, 'username': username} for userID, username in banned_list], 200
    
    @api.response(201, 'Success')
    @api.response(400, 'userID must be a non-negative integer')
    @api.response(401, 'Authentication token is missing')
    @api.response(403,
                  "Either this reviewer already exists in the user's Banned List, "
                  'or the user has attempted to add himself to his own Banned List'
                 )
    @api.response(404, 'Reviewer was not found')
    @api.expect(banned_user)
    def post(self):
        '''
        Add a FilmFinder to your Banned List.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        is_valid_integer(request.json['userID'])
        session = Session()
        query = session.query(User).filter(User.userID == request.json['userID']).one_or_none()
        if not query:
            raise NotFound
        query = session.query(Bannedlist).filter(Bannedlist.userID == g.userID,
                                                 Bannedlist.bannedUserID == request.json['userID']
                                                ).one_or_none()
        if query or g.userID == request.json['userID']:
            raise Forbidden
        session.add(Bannedlist(g.userID, request.json['userID']))
        session.commit()
        return {'message': 'Reviewer banned.'}, 201

    @api.response(200, 'Success')
    @api.response(400, 'userID must be a non-negative integer')
    @api.response(401, 'Authentication token is missing')
    @api.response(404, 'Reviewer was not found in Banned List')
    @api.expect(banned_user)
    def delete(self):
        '''
        Remove a FilmFinder from your Banned List.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        is_valid_integer(request.json['userID'])
        session = Session()
        if not session.query(Bannedlist).filter(Bannedlist.userID == g.userID,
                                                Bannedlist.bannedUserID == request.json['userID']
                                               ).delete():
            session.commit()
            raise NotFound
        session.commit()
        return {'message': 'Reviewer unbanned.'}, 200
