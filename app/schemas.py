
from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class Post(PostBase):
    pass

class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True