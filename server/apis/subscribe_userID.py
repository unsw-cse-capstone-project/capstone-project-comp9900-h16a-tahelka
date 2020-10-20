from flask import request, g
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound

from authentication.token_authenticator import TokenAuthenticator
from db_engine import Session
from models.Subscription import Subscription

api = Namespace('Subscribe', path='/subscribeUsers')

@api.route('/<int:userID>')
class SubscribeUsersID(Resource):
    @api.response(204, "User unsubscribed.")
    @api.response(404, "The parameters submitted are not found")
    def delete(self, userID):
        '''
        Unsubscribe to said user.
        '''
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        session = Session()

        affectedRows = session.query(Subscription).filter(Subscription.userID == g.userID) \
            .filter(Subscription.subscribedUserID == userID).delete()

        # When 0, it means userIDs are not present in database.
        if affectedRows == 0:
            raise NotFound
        else:
            session.commit()

        return 204
