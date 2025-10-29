from pydantic import BaseModel

class ParableBase(BaseModel):
    title: str
    reference: str | None = None
    summary: str

class ParableCreate(ParableBase):
    pass

class ParableUpdate(BaseModel):
    title: str | None = None
    reference: str | None = None
    summary: str | None = None

class ParableOut(ParableBase):
    id: int

    class Config:
        orm_mode = True
