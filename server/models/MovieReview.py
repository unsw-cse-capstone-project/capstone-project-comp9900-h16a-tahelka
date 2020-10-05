from sqlalchemy import Column, Integer, String, ForeignKey
from models.Common import Base


class MovieReview(Base):
    __tablename__ = "movieReviews"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.userID"), primary_key=True, index=True)
    rating = Column(Integer, index=True)
    review = Column(String)

    def __init__(self, movieID, userID):
        self.movieID = movieID
        self.userID = userID