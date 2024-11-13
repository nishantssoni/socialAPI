from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False

@app.get("/")
async def root():
    return {"message": "Hello World...nishant"}

@app.get("/posts/")
async def posts():
    return {"message": "This is a post"}

@app.post("/createpost/")
async def createpost(post: Post):
    print(post)
    return {"new_data": "post created"}