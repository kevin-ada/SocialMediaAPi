from typing import Optional

from pydantic import BaseModel, EmailStr
import datetime

from pydantic.types import conint


class PostBase(BaseModel):
    content:str
    title:str

    class Config:
        orm_mode = True


class UserOutput(BaseModel):
    email: EmailStr
    id: int
    created_at:datetime.datetime
    class Config:
        orm_mode = True

class GetallPosts(BaseModel):
    content: str
    title: str
    id:int
    owner_id:int
    owner:UserOutput
    class Config:
        orm_mode = True


class OrmPostout(BaseModel):
    Post:GetallPosts
    votes:int

    class Config:
        orm_mode = True



class CreatePost(PostBase):
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email:str
    password:str

class UserLogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class DataToken(BaseModel):
    id:Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir:conint(ge=0, le=1)
