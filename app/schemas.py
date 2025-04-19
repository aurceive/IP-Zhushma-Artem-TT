from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
  name: str
  surname: str
  password: str

class UserRead(BaseModel):
  id: int
  name: str
  surname: str
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True

class UserUpdate(BaseModel):
  name: str | None = None
  surname: str | None = None
  password: str | None = None
