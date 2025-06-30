from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MastersGymer(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    photo: Optional[str] = None
    gymer_id: int
    
    model_config = ConfigDict(from_attributes=True)
    

class Gymer(BaseModel):
    gymer_id: int
    user_id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
    

class Master(BaseModel):
    master_id: int
    user_id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
    
class UserBase(BaseModel):
    user_id: int
    username: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    telegram_id: int
    photo: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):    
    master: Optional[Master] = None
    gymer: Optional[Gymer] = None
    
    model_config = ConfigDict(from_attributes=True)
    

class UserIn(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    telegram_id: int
    photo: Optional[str] = None
    