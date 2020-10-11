from sqlalchemy import Column, Integer, String
from models.Common import Base


class User(Base):
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    yob = Column(Integer)

    def __init__(self, username, email, password, yob):
        self.username = username
        self.email = email
        self.password = password
        self.yob = yob
