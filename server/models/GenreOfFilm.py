from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.Common import Base

class GenreOfFilm(Base):
    __tablename__ = "genreOfFilm"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True)
    genreID = Column(Integer, ForeignKey("genres.genreID"), primary_key= True)

    def __init__(self, movieID, genreID):
        self.movieID = movieID
        self.genreID = genreID
