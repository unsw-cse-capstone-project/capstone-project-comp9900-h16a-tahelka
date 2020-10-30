from db_engine import Session
from models.BannedList import BannedList
from models.Movie import Movie
from models.MovieReview import MovieReview


def compute(movieID, userID, ratings_sum = None, review_count = None):
    session = Session()
    if ratings_sum is None or review_count is None:
        query = session.query(Movie.ratings_sum,
                              Movie.review_count
                             ).filter(Movie.movieID == movieID).one_or_none()
        ratings_sum, review_count = query if query else (0, 0)
    banned_user_ratings\
        = session.query(MovieReview.rating)\
                 .filter(MovieReview.movieID == movieID,
                         MovieReview.userID.in_(session.query(BannedList.bannedUserID)
                                                       .filter(BannedList.userID == userID)
                                               )
                        ).all()
    review_count -= len(banned_user_ratings)
    return round((ratings_sum - sum(rating for rating, in banned_user_ratings))
                 / review_count,
                 1
                ) if review_count\
                  else 0.0
