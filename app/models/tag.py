from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.bookmark import bookmark_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    bookmarks = relationship("Bookmark", secondary=bookmark_tags, back_populates="tags")
