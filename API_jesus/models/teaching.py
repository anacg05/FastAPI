from sqlalchemy import Column, Integer, String, Text
from core.db import Base

class Teaching(Base):
    __tablename__ = "teachings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    source = Column(String(100))
    content = Column(Text, nullable=False)
