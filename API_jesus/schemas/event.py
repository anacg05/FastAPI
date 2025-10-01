from pydantic import BaseModel
from typing import Optional

class EventBase(BaseModel):
    title: str
    reference: str
    description: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    reference: Optional[str] = None
    description: Optional[str] = None

class EventOut(EventBase):
    id: int
    class Config:
        from_attributes = True
