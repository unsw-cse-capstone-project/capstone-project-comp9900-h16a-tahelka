from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.Common import Base

class Wishlist(Base):
    __tablename__ = "wishlists"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True)
    userID = Column(Integer, ForeignKey("filmFinders.userID"), primary_key=True)

    def __init__(self, movieID, userID):
        self.movieID = movieID
        self.userID = userID