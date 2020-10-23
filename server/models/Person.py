from sqlalchemy import Column, Integer, String
from models.Common import Base


class Person(Base):
    __tablename__ = "persons"

    personID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name
