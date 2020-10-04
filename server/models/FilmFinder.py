from sqlalchemy import Column, Integer, String
from models.Common import Base


class FilmFinder(Base):
    __tablename__ = "filmFinders"

    userID = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    yob = Column(Integer)

    def __init__(self, username, email, password_hash, yob):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.yob = yob
