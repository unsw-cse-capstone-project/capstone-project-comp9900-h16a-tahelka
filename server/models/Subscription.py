from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.Common import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    userID = Column(Integer, ForeignKey("filmFinders.userID"),
                    primary_key=True)
    subscribedUserID = Column(Integer, ForeignKey("filmFinders.userID"),
                              primary_key=True)

    def __init__(self, userID, subscribedUserID):
        self.userID = userID
        self.subscribedUserID = subscribedUserID
