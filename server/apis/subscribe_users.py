from flask import request, g
from flask_restx import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Subscription import Subscription

api = Namespace('Subscribe', path='/subscribeUsers')

subscribe_model = api.model('Subscribe', {
    'userID': fields.Integer(description='Identifier of user'),
})


@api.route('')
class SubscribeUsers(Resource):

    @api.expect(subscribe_model)
    @api.response(201, "Subscribed to User")
    @api.response(400, "The parameters submitted are invalid.")
    def post(self):
        '''
            Subscribe to the user.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        subscribedUserID = request.json.get('userID')
        curUserID = g.userID

        # Can't subscribe to oneself.
        if curUserID == subscribedUserID:
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