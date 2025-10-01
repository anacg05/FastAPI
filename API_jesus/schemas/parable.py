from pydantic import BaseModel
from typing import Optional

class ParableBase(BaseModel):
    title: str
    reference: str
    summary: str

class ParableCreate(ParableBase):
    pass

class ParableUpdate(BaseModel):
    title: Optional[str] = None
    reference: Optional[str] = None
    summary: Optional[str] = None

class ParableOut(ParableBase):
    id: int
    class Config:
        from_attributes = True
