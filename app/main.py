from fastapi import FastAPI, status, HTTPException
from . import schemas
from . import models
from . import utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List



# initializing

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# routes
@app.get("/")
async def root():
    return {"message": "Hello World...nishant"}


# posts routes
@app.get("/posts/", response_model=List[schemas.PostResponse])
async def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def getpost(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post


@app.post("/posts/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def createpost(post: schemas.Post, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.delete("/posts/{id}", response_model=schemas.PostResponse)
async def deletepost(id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    db.delete(db_post)
    db.commit()
    return db_post


@app.put("/posts/{id}", response_model=schemas.PostResponse) 
async def updatepost(id: int, post: schemas.Post, db: Session = Depends(get_db)):  
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")    
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post


# routes for users
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def createuser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
