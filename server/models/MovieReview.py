from sqlalchemy import Column, Integer, Float, String, ForeignKey
from models.Common import Base
from time import time


class MovieReview(Base):
    __tablename__ = "movieReviews"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.userID"), primary_key=True, index=True)
    rating = Column(Float, index=True)
    review = Column(String, nullable=False)
    timestamp = Column(Float)

    def __init__(self, movieID, userID, rating, review):
        self.movieID = movieID
        self.userID = userID
        self.rating = rating
        self.review = review
        self.timestamp = time()
