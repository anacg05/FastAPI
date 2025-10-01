from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base

class Parable(Base):
    __tablename__ = "parables"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    reference: Mapped[str] = mapped_column(String(100))
    summary: Mapped[str] = mapped_column(Text)
