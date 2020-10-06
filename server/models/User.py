from sqlalchemy import Column, Integer, String
from models.Common import Base


class User(Base):
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    yob = Column(Integer)

    def __init__(self, username, email, password, yob):
        self.username = username
        self.email = email
        self.password = password
        self.yob = yob
