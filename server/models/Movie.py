from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from db_engine import Session
from models.Common import Base
from models.BannedList import BannedList
from models.MovieReview import MovieReview
from sqlalchemy.sql import text

class Movie(Base):
    __tablename__ = 'movies'

    movieID = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String)
    ratings_sum = Column(Float)
    review_count = Column(Integer)

    def __init__(self, title, year, description, ratings_sum, review_count):
        self.title = title
        self.year = year
        self.description = description
        self.ratings_sum = ratings_sum
        self.review_count = review_count

    @hybrid_method
    def average_rating(): pass
    '''
    def average_rating(self, userID):
        session = Session()
        banned_user_ratings\
            = session.query(MovieReview.rating)\
                     .filter(MovieReview.movieID == self.movieID,
                             MovieReview.userID.in_(session.query(BannedList.bannedUserID)
                                                           .filter(BannedList.userID == userID)
                                                   )
                            ).all()
        review_count = Movie.review_count - len(banned_user_ratings)
        return round((Movie.ratings_sum - sum(rating for rating, in banned_user_ratings))
                     / review_count,
                     1
                    ) if review_count\
                      else 0.0
    '''

    @average_rating.expression
    def average_rating(cls, userID):
        banned_users = f'SELECT bannedlists.bannedUserID FROM bannedlists WHERE bannedlists.userID = {userID}'
        banned_users_review_count = f'SELECT count(*) FROM movieReviews WHERE movieReviews.movieID = movies.movieID AND movieReviews.userID IN ({banned_users})'
        banned_users_ratings_sum = f'SELECT coalesce(sum(movieReviews.rating), 0) FROM movieReviews WHERE movieReviews.movieID = movies.movieID AND movieReviews.userID IN ({banned_users})'
        return text(f'round(CASE WHEN movies.review_count - ({banned_users_review_count}) = 0 THEN 0'
                              f' ELSE (movies.ratings_sum - ({banned_users_ratings_sum})) / (movies.review_count - ({banned_users_review_count}))'
                          ' END,'
                          ' 1'
                          ')'
                   )
        '''
        return CASE WHEN movies.review_count - (SELECT count(*)
                                                FROM movieReviews
                                                WHERE movieReviews.movieID = movies.movieID
                                                      AND movieReviews.userID IN (SELECT bannedlists.bannedUserID
                                                                                  FROM bannedlists
                                                                                  WHERE bannedlists.userID = userID
                                                                                 )
                                               ) = 0 THEN 0.0
                    ELSE (movies.ratings_sum - (SELECT sum(movieReviews.rating)
                                                FROM movieReviews
                                                WHERE movieReviews.movieID = movies.movieID
                                                      AND movieReviews.userID IN (SELECT bannedlists.bannedUserID
                                                                                  FROM bannedlists
                                                                                  WHERE bannedlists.userID = userID
                                                                                 )
                                               )
                         ) / (movies.review_count - (SELECT count(*)
                                                     FROM movieReviews
                                                     WHERE movieReviews.movieID = movies.movieID
                                                           AND movieReviews.userID IN (SELECT bannedlists.bannedUserID
                                                                                       FROM bannedlists
                                                                                       WHERE bannedlists.userID = userID
                                                                                      )
                                                    )
                             )
               END
        
        return case({cls.review_count - (subquery_1): 0.0},
                    0,
                    (cls.ratings_sum - func.sum(subquery_2)) / cls.review_count - (subquery_1)
                   )
        '''
