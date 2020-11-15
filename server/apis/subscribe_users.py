from flask import request, g
from flask_restx import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Subscription import Subscription
from models.User import User

api = Namespace('Subscribe', path='/subscribeUsers',
                description='CRUD Subscribed Users')

subscribe_model = api.model('Subscribe', {
    'userID': fields.Integer(description='Identifier of user'),
})

subscribed_users = api.model('Subscribed Reviewer', {'userID': fields.Integer,
                                            'username': fields.String})
subscribed_users_list = api.model('List',
                                  {
                                      'subscribedUsers': fields.List(fields.Nested(subscribed_users))
                                  })
@api.route('')
class SubscribeUsers(Resource):

    @api.expect(subscribe_model)
    @api.response(201, "Subscribed to User")
    @api.response(400, "The parameters submitted are invalid.")
    @api.response(401, 'Authentication token is missing')
    def post(self):
        '''
            Subscribe to the user.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        subscribedUserID = request.json.get('userID')
        curUserID = g.userID

        # Can't subscribe to oneself.
        if curUserID == int(subscribedUserID):
            raise BadRequest

        subscribe = Subscription(curUserID, subscribedUserID)
        session = Session()
        session.add(subscribe)
        try:
            session.commit()
        except IntegrityError:  #If subscription already present
            session.rollback()
            raise BadRequest

        response = {'message':'Subscribed to User'}
        return response, 201

    @api.response(200, 'List of subscribed users', subscribed_users_list)
    @api.response(401, 'Authentication token is missing')
    def get(self):
        '''
        Show list of subscribed users
        '''

        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()


        results = session.query(Subscription.subscribedUserID, User.username) \
            .filter(Subscription.userID == g.userID) \
            .filter(User.userID == Subscription.subscribedUserID)

        users = list()
        for id, username in results:
            users.append({'userID': id, 'username': username})

        response = {'subscribedUsers':users}
        return response, 200

