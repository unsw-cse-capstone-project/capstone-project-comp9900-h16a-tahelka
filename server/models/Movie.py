from sqlalchemy import Column, Integer, String, Float
from models.Common import Base

class Movie(Base):
    __tablename__ = 'movies'

    movieID = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(String, nullable=False)
    description = Column(String)
    ratings_sum = Column(Float)
    review_count = Column(Integer)

    def __init__(self, title, year, description, ratings_sum, review_count):
        self.title = title
        self.year = year
        self.description = description
        self.ratings_sum = ratings_sum
        self.review_count = review_count
