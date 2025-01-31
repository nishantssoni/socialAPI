from fastapi import FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
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
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:    
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Voted successfully "}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"user {current_user.id} has not voted on post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
    return {"message": "Voted successfully"}