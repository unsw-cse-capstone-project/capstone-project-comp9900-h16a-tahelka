from flask import request, g
from flask_restx import Namespace, fields, Resource
from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.BannedList import BannedList
from models.Subscription import Subscription
from models.User import User
from werkzeug.exceptions import Forbidden, NotFound
from util.IntValidations import is_valid_integer


api = Namespace('Banned List', 'CRUD Bannedlist of users', '/bannedlists')

banned_user = api.model('Banned Reviewer', {'userID': fields.Integer, 'username': fields.String})

user_to_ban = api.model('Reviewer to Ban', {'userID': fields.Integer})

@api.route('')
class BannedLists(Resource):
    @api.response(200, 'Success', [banned_user])
    @api.response(401, 'Authentication token is missing')
    def get(self):
        '''
        View your Banned List.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        banned_list = Session().query(User.userID, User.username)\
                               .join(BannedList, User.userID == BannedList.bannedUserID)\
                               .filter(BannedList.userID == g.userID)
        return [{'userID': userID, 'username': username} for userID, username in banned_list], 200
    
    @api.response(201, 'Success')
    @api.response(400, 'userID must be a non-negative integer')
    @api.response(401, 'Authentication token is missing')
    @api.response(403,
                  "Either this reviewer already exists in the user's Banned List, "
                  'or the user has attempted to add himself to his own Banned List'
                 )
    @api.response(404, 'Reviewer was not found')
    @api.expect(user_to_ban)
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
        query = session.query(BannedList).filter(BannedList.userID == g.userID,
                                                 BannedList.bannedUserID == request.json['userID']
                                                ).one_or_none()
        if query or g.userID == request.json['userID']:
            # If the FilmFinder being banned is already in the user's Banned List,
            # or if a user is attempting to ban himself, raise an Exception.
            raise Forbidden
        # Remove a user's subscription to a FilmFinder when banning that FilmFinder.
        session.query(Subscription).filter(Subscription.userID == g.userID,
                                           Subscription.subscribedUserID == request.json['userID']
                                          ).delete()
        session.add(BannedList(g.userID, request.json['userID']))
        session.commit()
        session.close()
        return {'message': 'Reviewer banned.'}, 201
