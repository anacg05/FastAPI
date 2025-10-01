from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base

class Teaching(Base):
    __tablename__ = "teachings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    source: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)