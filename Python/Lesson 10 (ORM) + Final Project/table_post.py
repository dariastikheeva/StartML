from database import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)
	 
if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session = SessionLocal()

    result = [
        i.id for i in (
            session.query(Post)
            .filter(Post.topic == 'business')
            .order_by(Post.id.desc())
            .limit(10)
	        .all()
        )
    ]

    print(result)