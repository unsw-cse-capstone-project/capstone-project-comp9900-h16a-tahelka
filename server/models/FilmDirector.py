from sqlalchemy import Column, Integer, ForeignKey, String

from models.Common import Base


class FilmDirector(Base):
    __tablename__ = "filmDirectors"

    movieID = Column(Integer, ForeignKey("movies.movieID"), primary_key=True)
    personID = Column(Integer, ForeignKey("persons.personID"), primary_key=True)
    bio = Column(String)

    def __init__(self, movieID, personID, bio):
        self.movieID = movieID
        self.personID = personID
        self.bio = bio
