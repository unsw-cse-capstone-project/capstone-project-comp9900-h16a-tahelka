from sqlalchemy import Column, Integer, String, Float
from models.Common import Base

class Movie(Base):
    __tablename__ = 'movies'

    movieID = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    description = Column(String)
    avg_rating = Column(Float)
    total_ratings = Column(Integer)

    def __init__(self, title, year, description, avg_rating, total_ratings):
        self.title = title
        self.year = year
        self.description = description
        self.avg_rating = avg_rating
        self.total_ratings = total_ratings