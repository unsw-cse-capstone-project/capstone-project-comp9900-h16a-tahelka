from sqlalchemy import Column, Integer, Float, String, ForeignKey
from models.Common import Base


class MovieReview(Base):
    __tablename__ = "movieReviews"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.userID"), primary_key=True, index=True)
    rating = Column(Float, index=True)
    review = Column(String)
    timestamp = Column(Float)

    def __init__(self, movieID, userID, rating, review, timestamp):
        self.movieID = movieID
        self.userID = userID
        self.rating = rating
        self.review = review
        self.timestamp = timestamp
