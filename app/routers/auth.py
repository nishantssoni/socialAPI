from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent  # Goes up one level from 'routers'
sys.path.insert(0, str(ROOT_DIR))
import database
import models
import schemas
import utils

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user not found")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user not found")
    
    # create a token
    return {"token ": "token"}