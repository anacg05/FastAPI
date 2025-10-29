from pydantic import BaseModel

class EventBase(BaseModel):
    title: str
    reference: str | None = None
    description: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: str | None = None
    reference: str | None = None
    description: str | None = None

class EventOut(EventBase):
    id: int

    class Config:
        orm_mode = True
