from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import BookmarkNotFoundError, DuplicateBookmarkError
from app.schemas.bookmark import BookmarkCreate, BookmarkRead, BookmarkUpdate
from app.services import bookmark_service

router = APIRouter()


def _to_read(b) -> BookmarkRead:
    return BookmarkRead(
        id=b.id,
        url=b.url,
        title=b.title,
        description=b.description,
        created_at=b.created_at,
        tags=[t.name for t in b.tags],
    )


@router.post("", response_model=BookmarkRead, status_code=status.HTTP_201_CREATED)
def create(data: BookmarkCreate, db: Session = Depends(get_db)):
    try:
        bookmark = bookmark_service.create_bookmark(db, data)
    except DuplicateBookmarkError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return _to_read(bookmark)


@router.get("", response_model=List[BookmarkRead])
def list_all(tag: Optional[str] = None, db: Session = Depends(get_db)):
    return [_to_read(b) for b in bookmark_service.list_bookmarks(db, tag=tag)]


@router.get("/{bookmark_id}", response_model=BookmarkRead)
def get_one(bookmark_id: int, db: Session = Depends(get_db)):
    try:
        bookmark = bookmark_service.get_bookmark(db, bookmark_id)
    except BookmarkNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return _to_read(bookmark)


@router.patch("/{bookmark_id}", response_model=BookmarkRead)
def update(bookmark_id: int, data: BookmarkUpdate, db: Session = Depends(get_db)):
    try:
        bookmark = bookmark_service.update_bookmark(db, bookmark_id, data)
    except BookmarkNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return _to_read(bookmark)


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(bookmark_id: int, db: Session = Depends(get_db)):
    try:
        bookmark_service.delete_bookmark(db, bookmark_id)
    except BookmarkNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
