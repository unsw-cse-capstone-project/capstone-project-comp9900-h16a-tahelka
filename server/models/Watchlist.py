from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.Common import Base

class Watchlist(Base):
    __tablename__ = "watchlists"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True)
    userID = Column(Integer, ForeignKey("users.userID"), primary_key=True)

    def __init__(self, movieID, userID):
        self.movieID = movieID
        self.userID = userID