from flask import request, g, current_app
from flask_restx import Namespace, fields, Resource, reqparse

from RecSystem.rec_calc import movie_similarity_calc
from authentication.token_authenticator import TokenAuthenticator
from util.IntValidations import is_valid_integer
from db_engine import Session
from models.Movie import Movie
from models.BannedList import BannedList
from util.RatingCalculator import compute
from sqlite3 import ProgrammingError

api = Namespace('Movies', path = '/movies',
                description='Get Movie Recommendations')

parser = reqparse.RequestParser()
parser.add_argument('use_genre', required= False, type = int, default=1)
parser.add_argument('use_director', required= False, type = int, default=1)
movie_details = api.model('movie',
                                 {'movieID': fields.Integer,
                                  'title': fields.String,
                                  'year': fields.Integer,
                                  'rating': fields.Float(description = 'Average rating out of 5')
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
        topMovieIds = list()
        movies = list()

        # Need this try/except block to catch errors when calling
        # recommendations if dataframes haven't loaded yet.
        try:
            movie = current_app.movieDf
            director = current_app.dirDf
            genre = current_app.genDf
            user = current_app.userDf

            topMovieIds = movie_similarity_calc(movieID=movieID, userID=userID, movie=movie, director=director, genre=genre, user=user,
                                          use_genre=use_genre, use_director=use_director)

            session = Session()
            result = session.query(Movie.movieID, Movie.title, Movie.year, Movie.ratings_sum,
                                   Movie.review_count).filter(Movie.movieID.in_(topMovieIds)).all()

            banned_users = tuple(banned_user for banned_user, in session.query(BannedList.bannedUserID)\
                                 .filter(BannedList.userID == userID))


            for id, title, year, ratings_sum, review_count in result:
                movies.append({'movieID': id, 'title': title, 'year': year,
                               'rating': compute(movieID, g.userID, ratings_sum, review_count, banned_users)})

            movies.sort(key = lambda film: (-film['rating'], film['title']))
        
        except ProgrammingError as pe:
            print("Df hasn't loaded yet.")

        except Exception as e:
            print("Df hasn't loaded yet.")

        response = {'movies': movies}
        return response, 200


