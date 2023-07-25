from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class Product(BaseModel):
    name: str
    price: int





class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostBase):
    class Config:
         from_attributes = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass





class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
         from_attributes = True