from sqlalchemy import Column, Integer, String, Text
from core.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    reference = Column(String(100))
    description = Column(Text, nullable=False)
