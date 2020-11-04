from flask import request, g, current_app
from flask_restx import Namespace, fields, Resource

from RecSystem.rec_calc import movie_similarity_calc
from authentication.token_authenticator import TokenAuthenticator
from util.IntValidations import is_valid_integer

api = Namespace('Movies', path = '/movies')

movie_recommendation = api.model('Movie Recommendation',
                                 {'movieID': fields.Integer,
                                  'title': fields.String,
                                  'year': fields.Integer
                                 }
                                )

@api.route('/<int:movieID>/recommendations')
@api.param('movieID', 'The Movie identifier')
class Recommendations(Resource):
    # @api.response(200, 'Success', movie_recommendation)
    @api.response(400, 'id must be a non-negative integer')
    @api.response(401, 'Authentication token is missing')
    @api.response(404, 'Movie was not found')
    def get(self, movieID):
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        is_valid_integer(movieID)

        userID = g.userID

        # TODO: change to fetch from request params
        use_genre = 1
        use_director = 1
        movie = current_app.movieDf
        director = current_app.dirDf
        genre = current_app.genDf
        user = current_app.userDf
        topMovies = movie_similarity_calc(movieID, userID, movie=movie, director=director, genre=genre, user=user,
                                          use_genre=use_genre, use_director=use_director)

        response = {'topMovies': topMovies}
        return response, 200


