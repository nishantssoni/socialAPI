
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class Post(PostBase):
    pass

class PostResponse(PostBase):
    created_at: datetime
    id: int

    class Config:
        orm_mode = True

# users

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int

    class Config:
        orm_mode = True

# auth
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None