from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet
import uvicorn

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

# @app.get('/user/{id}', response_model=UserGet)
# def get_user_id(id: int,  db: Session = Depends(get_db)) -> UserGet:
#     res = db.query(User).filter(User.id == id).one_or_none()
#     if res != None:
#         return res
#     else:
#         raise HTTPException(status_code=404, detail="user not found")
    
# @app.get('/post/{id}', response_model=PostGet)
# def get_user_id(id: int,  db: Session = Depends(get_db)) -> PostGet:
#     res = db.query(Post).filter(Post.id == id).one_or_none()
#     if res != None:
#         return res
#     else:
#         raise HTTPException(status_code=404, detail="post not found")
    
# @app.get("/user/{id}/feed", response_model=List[FeedGet])
# def user_id(id: int, limit: int = 10, db: Session = Depends(get_db)) -> FeedGet:
#     res = (
#         db.query(Feed)
#         .filter(Feed.user_id == id)
#         .order_by(desc(Feed.time))
#         .limit(limit)
#         .all()
#     )
#     if res != []:
#         return res
#     else:
#         raise HTTPException(status_code=200)
    
# @app.get("/post/{id}/feed", response_model=List[FeedGet])
# def post_id(id: int, limit: int = 10, db: Session = Depends(get_db)) -> FeedGet:
#     res = (
#         db.query(Feed)
#         .filter(Feed.post_id == id)
#         .order_by(desc(Feed.time))
#         .limit(limit)
#         .all()
#     )
#     if res != []:
#         return res
#     else:
#         raise HTTPException(status_code=200)
    
@app.get("/post/recommendations/", response_model=List[PostGet])
def user_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    res = (
        db.query(Post)
        .select_from(Feed)
        .filter(Feed.action == "like")
        .join(Post)
        .group_by(Post.id)
        .order_by(func.count(Post.id).desc())
        .limit(limit)
        .all()
    )
    return res
