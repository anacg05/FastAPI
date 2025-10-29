from sqlalchemy import Column, Integer, String, Text
from core.db import Base

class Parable(Base):
    __tablename__ = "parables"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    reference = Column(String(100))
    summary = Column(Text, nullable=False)
