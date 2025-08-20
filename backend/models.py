from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class SelfieResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True


class UserWithSelfies(UserResponse):
    selfies: List[SelfieResponse] = []