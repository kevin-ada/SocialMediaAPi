from pydantic import BaseModel

class PostBase(BaseModel):
    content:str
    title:str



class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

