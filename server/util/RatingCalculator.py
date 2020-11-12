from db_engine import Session
from models.BannedList import BannedList
from models.Movie import Movie
from models.MovieReview import MovieReview
from math import ceil, floor


def compute(movieID, userID, ratings_sum = None, review_count = None, banned_users = None):
    session = Session()
    if ratings_sum is None or review_count is None:
        query = session.query(Movie.ratings_sum,
                              Movie.review_count
                             ).filter(Movie.movieID == movieID).one_or_none()
        ratings_sum, review_count = query if query else (0, 0)
    if banned_users is None:
        banned_users = tuple(banned_user for banned_user, in session.query(BannedList.bannedUserID)
                                                                    .filter(BannedList.userID == userID)
                            )
    banned_user_ratings = session.query(MovieReview.rating)\
                                 .filter(MovieReview.movieID == movieID,
                                         MovieReview.userID.in_(banned_users)
                                        ).all()
    review_count -= len(banned_user_ratings)
    rating_times_ten = ((ratings_sum - sum(rating for rating, in banned_user_ratings)) / review_count)\
                       * 10\
                           if review_count\
                           else 0
    # This is to ensure multiples of 0.05 are always rounded up,
    # in contrast to the behaviour of Python's round() method.
    # Reference: <https://stackoverflow.com/questions/33019698/how-to-properly-round-up-half-float-numbers-in-python>
    return floor(rating_times_ten) / 10 if rating_times_ten - floor(rating_times_ten) < 0.5\
                                        else ceil(rating_times_ten) / 10
