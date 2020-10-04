from sqlalchemy import Column, Integer, String, Float
from models.Common import Base

class Genres(Base):
    __tablename__ = "genres"

    genreID = Column(Integer, primary_key= True)
    genre = Column(String)

    def __init__(self, genre):
        self.genre = genre