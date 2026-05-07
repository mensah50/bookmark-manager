from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.bookmark import Bookmark
from app.models.tag import Tag
from app.schemas.bookmark import BookmarkCreate, BookmarkUpdate
from app.core.errors import BookmarkNotFoundError, DuplicateBookmarkError


def _get_or_create_tags(db: Session, names: List[str]) -> List[Tag]:
    tags = []
    for name in names:
        tag = db.query(Tag).filter(Tag.name == name).first()
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
        tags.append(tag)
    return tags


def create_bookmark(db: Session, data: BookmarkCreate) -> Bookmark:
    bookmark = Bookmark(
        url=str(data.url),
        title=data.title,
        description=data.description,
    )
    bookmark.tags = _get_or_create_tags(db, data.tags)
    db.add(bookmark)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateBookmarkError(f"Bookmark with url {data.url} already exists")
    db.refresh(bookmark)
    return bookmark


def list_bookmarks(db: Session, tag: Optional[str] = None) -> List[Bookmark]:
    query = db.query(Bookmark)
    if tag:
        query = query.join(Bookmark.tags).filter(Tag.name == tag)
    return query.order_by(Bookmark.created_at.desc()).all()


def get_bookmark(db: Session, bookmark_id: int) -> Bookmark:
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not bookmark:
        raise BookmarkNotFoundError(f"Bookmark {bookmark_id} not found")
    return bookmark


def update_bookmark(db: Session, bookmark_id: int, data: BookmarkUpdate) -> Bookmark:
    bookmark = get_bookmark(db, bookmark_id)
    if data.title is not None:
        bookmark.title = data.title
    if data.description is not None:
        bookmark.description = data.description
    if data.tags is not None:
        bookmark.tags = _get_or_create_tags(db, data.tags)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def delete_bookmark(db: Session, bookmark_id: int) -> None:
    bookmark = get_bookmark(db, bookmark_id)
    db.delete(bookmark)
    db.commit()
