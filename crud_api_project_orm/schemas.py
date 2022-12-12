from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

"""
    Schemas (pydantic models) related to users
"""
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


"""
    Schemas (pydantic models) related to posts
"""
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostVotesResponse(BaseModel):
    Post: PostResponse
    votes: int


"""
    Schemas (pydantic models) related to Access Token
"""
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


"""
    Schemas (pydantic models) related to Voting System
"""
class Vote(BaseModel):
    post_id: int
    dir: bool