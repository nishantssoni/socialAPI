from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os

app = FastAPI()
# Load the .env file
load_dotenv()

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



my_posts = [
    {"title": "title of post 1", "content": "content of post 1","published": True,"rating": 4, "id": 1},
    {"title": "title of post 2", "content": "content of post 2","published": True,"rating": 5, "id": 2},
    {"title": "title of post 3", "content": "content of post 3","published": True,"rating": 5, "id": 3},]


class Post(BaseModel):
    title: str
    content: str
    published: bool = False

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
    for index, p in enumerate(my_posts):
        if p["id"] == id:
            my_posts[index] = post.dict()
            my_posts[index]["id"] = id
            return {"data": my_posts[index]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with id: {id} was not found")
