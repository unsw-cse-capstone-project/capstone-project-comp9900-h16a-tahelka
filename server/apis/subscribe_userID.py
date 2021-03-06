from flask import request, g
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound, BadRequest

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Subscription import Subscription

api = Namespace('Subscribe', path='/subscribeUsers')

@api.route('/<int:userID>')
class SubscribeUsersID(Resource):
    @api.response(204, "User unsubscribed.")
    @api.response(404, "The parameters submitted are not found")
    @api.doc(params={'userID': 'Identifier of user'})
    def delete(self, userID):
        '''
        Unsubscribe to said user.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        curUserID = g.userID

        # Can't subscribe to oneself.
        if curUserID == int(userID):
            raise BadRequest

        affectedRows = session.query(Subscription).filter(Subscription.userID == curUserID) \
            .filter(Subscription.subscribedUserID == userID).delete()

        # When 0, it means userIDs are not present in database.
        if affectedRows == 0:
            raise NotFound
        else:
            session.commit()

        return 204
