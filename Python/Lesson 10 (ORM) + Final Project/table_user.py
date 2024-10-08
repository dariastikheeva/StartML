from database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String, func, desc

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    os = Column(String)
    source = Column(String)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session = SessionLocal()

    result = [(i.country, i.os, i.ct) for i in (
        session.query(User.country, User.os, func.count('*').label('ct'))
        .filter(User.exp_group == 3)
        .group_by(User.country, User.os)
        .having(func.count('*') > 100)
        .order_by(desc('ct'))
        .all()
        )
    ]
    print(result)