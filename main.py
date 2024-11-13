from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


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
        
    return {"message": "post not found"}

@app.post("/posts/")
async def createpost(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"message": post_dict}

@app.put("/posts/{id}")
async def updatepost(id: int, post: Post):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts[i] = post.dict()
            return {"message": post.dict()}
            