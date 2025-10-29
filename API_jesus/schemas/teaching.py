from pydantic import BaseModel

class TeachingBase(BaseModel):
    title: str
    source: str | None = None
    content: str

class TeachingCreate(TeachingBase):
    pass

class TeachingUpdate(BaseModel):
    title: str | None = None
    source: str | None = None
    content: str | None = None

class TeachingOut(TeachingBase):
    id: int

    class Config:
        orm_mode = True
