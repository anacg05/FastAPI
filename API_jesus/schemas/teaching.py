from pydantic import BaseModel
from typing import Optional

class TeachingBase(BaseModel):
    title: str
    source: Optional[str] = None
    content: str

class TeachingCreate(TeachingBase):
    pass

class TeachingUpdate(BaseModel):
    title: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None

class TeachingOut(TeachingBase):
    id: int
    class Config:
        from_attributes = True