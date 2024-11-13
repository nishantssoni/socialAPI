from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random


app = FastAPI()

my_posts = [
    {"title": "title of post 1", "content": "content of post 1","published": True,"rating": 4, "id": 1},
    {"title": "title of post 2", "content": "content of post 2","published": True,"rating": 5, "id": 2},
    {"title": "title of post 3", "content": "content of post 3","published": True,"rating": 5, "id": 3},]


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World...nishant"}

@app.get("/posts/")
async def posts():
    return {"message": my_posts}

@app.get("/posts/{id}")
async def getpost(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with id: {id} was not found")


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def createpost(post: Post):
    post_dict = post.dict()
    post_dict["id"] = random.randint(0, 100000000)
    my_posts.append(post_dict)
    return {"message": post_dict}

@app.delete("/posts/{id}")
async def deletepost(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with id: {id} was not found")

@app.put("/posts/{id}")
async def updatepost(id: int, post: Post):
    for index, p in enumerate(my_posts):
        if p["id"] == id:
            my_posts[index] = post.dict()
            my_posts[index]["id"] = id
            return {"message": f"post with id: {id} was updated"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with id: {id} was not found")
