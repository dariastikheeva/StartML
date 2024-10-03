from fastapi import FastAPI, HTTPException, Depends
from datetime import date, timedelta
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True

def get_db():
    return psycopg2.connect(
    "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
    cursor_factory=RealDictCursor
    )

@app.get("/post/{id}", response_model=PostResponse)
def get_user(id: int, db = Depends(get_db)) -> PostResponse:

    with db.cursor() as cursor:
    
        cursor.execute(
                '''
                SELECT id, text, topic 
                FROM "post" 
                WHERE id=%(user_id)s
                ''',
                {"user_id": id,}
                )
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail='user not found')
        else:
            return PostResponse(**result)
