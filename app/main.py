from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


load_dotenv()  # Load the .env file

# Database connection
while True:
    try:
        conn = psycopg2.connect(
            host = os.getenv("HOST"),
            database = os.getenv("DATABASE"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


# model definitions
class Post(BaseModel):
    title: str
    content: str
    published: bool = False

# database operations
@app.get("/")
async def root():
    return {"message": "Hello World...nishant"}


@app.get("/posts/")
async def posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"message": posts}


@app.get("/posts/{id}")
async def getpost(id: int):
    cursor.execute("""select * from posts where id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"message": post}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def createpost(post: Post):
    cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning *""", 
                                            (post.title, post.content, post.published))
    my_post = cursor.fetchone()
    conn.commit()
    return {"message": my_post}


@app.delete("/posts/{id}")
async def deletepost(id: int):
    cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"message": deleted_post}


@app.put("/posts/{id}")
async def updatepost(id: int, post: Post):
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""",
                    (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"message": updated_post}
