from flask import request, g, current_app
from flask_restx import Namespace, fields, Resource, reqparse

from RecSystem.rec_calc import movie_similarity_calc
from authentication.token_authenticator import TokenAuthenticator
from util.IntValidations import is_valid_integer
from db_engine import Session
from models.Movie import Movie

api = Namespace('Movies', path = '/movies',
                description='Get Movie Recommendations')

parser = reqparse.RequestParser()
parser.add_argument('use_genre', required= False, type = int, default=1)
parser.add_argument('use_director', required= False, type = int, default=1)
movie_details = api.model('movie',
                                 {'movieID': fields.Integer,
                                  'title': fields.String,
                                  'year': fields.Integer
                                 }
                                )
results = api.model('movies',
                    {'movies':fields.List(fields.Nested(movie_details))}
                    )
@api.route('/<int:movieID>/recommendations')
@api.param('movieID', 'The Movie identifier')
class Recommendations(Resource):
    @api.response(200, 'Success', results)
    @api.response(400, 'id must be a non-negative integer')
    @api.response(401, 'Authentication token is missing')
    @api.response(404, 'Movie was not found')
    @api.expect(parser, validate=True)
    def get(self, movieID):
        TokenAuthenticator(request.headers.get('Authorization')).authenticate()
        is_valid_integer(movieID)

        userID = g.userID
        args = parser.parse_args()

        use_genre = args.get('use_genre')
        use_director = args.get('use_director')
        movie = current_app.movieDf
        director = current_app.dirDf
        genre = current_app.genDf
        user = current_app.userDf
        topMovieIds = movie_similarity_calc(movieID, userID, movie=movie, director=director, genre=genre, user=user,
                                          use_genre=use_genre, use_director=use_director)

        session = Session()
        result = session.query(Movie.movieID, Movie.title,
                              Movie.year).filter(Movie.movieID.in_(topMovieIds)).all()

        movies = list()
        for id, title, year in result:
            movies.append({'movieID': id, 'title': title, 'year': year})

        response = {'movies': movies}
        return response, 200


