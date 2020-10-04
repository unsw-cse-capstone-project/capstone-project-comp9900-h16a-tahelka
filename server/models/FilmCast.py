from sqlalchemy import Column, Integer, ForeignKey
from models.Common import Base


class FilmCast(Base):
    __tablename__ = "filmCast"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True)
    personID = Column(Integer, ForeignKey("persons.personID"), primary_key=True)

    def __init__(self, movieID, personID):
        self.movieID = movieID
        self.personID = personID