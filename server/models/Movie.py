from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.hybrid import hybrid_method
from db_engine import Session
from models.Common import Base
from models.BannedList import BannedList
from models.MovieReview import MovieReview
from sqlalchemy import case, func
from sqlalchemy.sql import select, and_

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
    This method is required by the method below.
    '''

    @average_rating.expression
    def average_rating(cls, userID):
        '''
        This method enables a movie's average rating, free of the influence
        of banned users, to be determined during a database query.
        '''
        banned_users = tuple(banned_user
                                 for banned_user,
                                     in Session().query(BannedList.bannedUserID)
                                                 .filter(BannedList.userID == userID)
                            )
        banned_users_review_count\
            = select([func.count()]).select_from(MovieReview)\
                                    .where(and_(MovieReview.movieID == cls.movieID,
                                                MovieReview.userID.in_(banned_users)
                                               )
                                          )
        banned_users_ratings_sum = select([func.coalesce(func.sum(MovieReview.rating),
                                           # This is necessary for a movie with no banned
                                                         0  # user ratings to be treated
                                                        )   # as having a sum of banned
                                          ]                 # user ratings of 0.
                                         ).where(and_(MovieReview.movieID == cls.movieID,
                                                      MovieReview.userID.in_(banned_users)
                                                     )
                                                )
        return case([(cls.review_count - banned_users_review_count == 0, 0)],
                    else_ = func.round((cls.ratings_sum - banned_users_ratings_sum)
                                       / (cls.review_count - banned_users_review_count),
                                       1
                                      )
                   )
