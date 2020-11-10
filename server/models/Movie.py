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

    @average_rating.expression
    def average_rating(cls, userID):
        # banned_users = select([BannedList.bannedUserID]).where(BannedList.userID == userID)
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
                                                         0
                                                        )
                                          ]
                                         ).where(and_(MovieReview.movieID == cls.movieID,
                                                      MovieReview.userID.in_(banned_users)
                                                     )
                                                )
        '''
        session = Session()
        banned_users = session.query(BannedList.bannedUserID).filter(BannedList.userID == userID)
        banned_users_review_count = session.query(MovieReview).filter(MovieReview.movieID == cls.movieID, MovieReview.userID.in_(banned_users)).count()
        banned_users_ratings_sum = session.query(func.sum(MovieReview.rating)).filter(MovieReview.movieID == cls.movieID, MovieReview.userID.in_(banned_users))
        '''
        return func.round(case([(cls.review_count - banned_users_review_count == 0, 0)],
                               else_ = (cls.ratings_sum - banned_users_ratings_sum)
                                       / (cls.review_count - banned_users_review_count)
                              ),
                          1
                         )
        '''
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
