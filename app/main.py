from fastapi import FastAPI, status, HTTPException
import schemas
import models
import utils
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from routers import users, posts, auth


# initializing

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)

# routes
@app.get("/")
async def root():
    return {"message": "Hello World...nishant soni"}

