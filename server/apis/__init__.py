from flask import Blueprint, g
from flask_restx import Api
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound

from apis.tokens import api as tokens
from apis.users import api as users
from apis.movie_search import api as movie_search
from apis.movie_details import api as movie_details

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

@api.errorhandler(BadRequest)
def handle_bad_request(error):
    # Analytics
    status_code = 400
    # Recorder('bad_request', status_code).recordUsage()

    response = {"message": "The request parameters are invalid."}
    return response, status_code

@api.errorhandler(NotFound)
def handle_not_found(error):
    # Analytics
    status_code = 404
    # Recorder('not_found_error', status_code).recordUsage()

    response = {"message": "Resource not found."}
    return response, status_code

@api.errorhandler(Unauthorized)
def handle_unauthorized(error):
    print(g)
    # Analytics
    status_code = 401
    # Recorder('unauthorized_error', status_code).recordUsage()

    response = {
        "message": "The provided credentials or token is incorrect or expired."
    }
    return response, status_code

@api.errorhandler(Forbidden)
def handle_forbidden(error):
    # Analytics
    status_code = 403
    # Recorder('forbidden_error', status_code).recordUsage()

    response = {
        "message": "You don't have permission to access this resource."
    }
    return response, status_code
