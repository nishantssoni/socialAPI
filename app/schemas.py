
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class Post(PostBase):
    pass