from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.Common import Base

class BannedList(Base):
    __tablename__ = "bannedlists"

    userID = Column(Integer, ForeignKey("users.userID"), primary_key=True,
                    index=True)
    bannedUserID = Column(Integer, ForeignKey("users.userID"), primary_key=True,
                          index=True)

    def __init__(self, userID, bannedUserID):
        self.userID = userID
        self.bannedUserID = bannedUserID
