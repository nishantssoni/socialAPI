from fastapi import FastAPI, status, HTTPException
from .schemas import Post
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends


models.Base.metadata.create_all(bind=engine)

app = FastAPI()




# database operations
@app.get("/")
async def root():
    return {"message": "Hello World...nishant"}


@app.get("/sqlalchemy")
async def sqla(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/")
async def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@app.get("/posts/{id}")
async def getpost(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"message": post}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def createpost(post: Post, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"data": db_post}


@app.delete("/posts/{id}")
async def deletepost(id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    db.delete(db_post)
    db.commit()
    return {"message": db_post}


@app.put("/posts/{id}") 
async def updatepost(id: int, post: Post, db: Session = Depends(get_db)):  
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")    
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return {"message": db_post}

