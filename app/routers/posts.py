from fastapi import FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
# At the top of your routers/user.py:
import sys
from pathlib import Path

# This line gets the absolute path to your root directory
ROOT_DIR = Path(__file__).parent.parent  # Goes up one level from 'routers'
sys.path.insert(0, str(ROOT_DIR))
import schemas
import models
from database import engine, get_db
import oauth2



router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)
# posts routes
@router.get("/", response_model=List[schemas.PostResponse])
async def posts(db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
async def getpost(id: int, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def createpost(post: schemas.Post, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{id}", response_model=schemas.PostResponse)
async def deletepost(id: int, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    db.delete(db_post)
    db.commit()
    return db_post


@router.put("/{id}", response_model=schemas.PostResponse) 
async def updatepost(id: int, post: schemas.Post, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)): 
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
