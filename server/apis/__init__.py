from flask import Blueprint, g
from flask_restx import Api
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound

from apis.tokens import api as tokens
from apis.users import api as users
from apis.movie_search import api as movie_search
from apis.movie_details import api as movie_details
from apis.movie_review import api as movie_review
from apis.wishlists import api as wishlists
from apis.wishlists_movieID import api as wishlists_movieID
from apis.wishlists_userID import api as wishlists_userID
from apis.banned_list import api as banned_list
from apis.banned_list_delete import api as banned_list_delete
from apis.subscribe_users import api as subscribe_users
from apis.subscribe_userID import api as subscribe_userID
from apis.subscribed_wishlist_movies import api as subscribed_wishlist_movies
from apis.wishlists_userID_import import api as wishlists_userID_import
from apis.watchlists import api as watchlists
from apis.watchlists_movieID import api as watchlists_movieID
from apis.recommendations import api as recommendations

blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')

authorizations = {
    'HTTP Bearer Authentication': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }
}

api = Api(
    blueprint,
    authorizations=authorizations,
    version='1.0',
    title='FilmFinder Service API',
    security='HTTP Bearer Authentication'
)

api.add_namespace(tokens)
api.add_namespace(users)
api.add_namespace(movie_search)
api.add_namespace(movie_details)
api.add_namespace(movie_review)
api.add_namespace(wishlists)
api.add_namespace(wishlists_movieID)
api.add_namespace(wishlists_userID)
api.add_namespace(banned_list)
api.add_namespace(banned_list_delete)
api.add_namespace(subscribe_users)
api.add_namespace(subscribe_userID)
api.add_namespace(subscribed_wishlist_movies)
api.add_namespace(wishlists_userID_import)
api.add_namespace(watchlists)
api.add_namespace(watchlists_movieID)
api.add_namespace(recommendations)

@api.errorhandler(BadRequest)
def handle_bad_request(error):
    status_code = 400
    response = {"message": "The request parameters are invalid."}
    return response, status_code

@api.errorhandler(NotFound)
def handle_not_found(error):
    status_code = 404
    response = {"message": "Resource not found."}
    return response, status_code

@api.errorhandler(Unauthorized)
def handle_unauthorized(error):
    print(g)
    status_code = 401
    response = {
        "message": "The provided credentials or token is incorrect or expired."
    }
    return response, status_code

@api.errorhandler(Forbidden)
def handle_forbidden(error):
    status_code = 403
    response = {
        "message": "You don't have permission to access this resource."
    }
    return response, status_code
