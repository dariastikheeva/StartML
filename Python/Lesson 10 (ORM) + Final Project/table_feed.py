from database import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from table_post import Post
from table_user import User
from sqlalchemy.orm import relationship

class Feed(Base):
    __tablename__ = "feed_action"
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    action = Column(String)
    time = Column(DateTime)
    user = relationship("User")
    post = relationship("Post")