import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.bookmark import Bookmark
from app.services.bookmark_service import get_bookmark
from app.core.errors import BookmarkNotFoundError


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    # Import models so they are registered on Base.metadata before create_all
    from app.models import bookmark, tag  # noqa: F401
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


def test_get_bookmark_returns_existing(session):
    bookmark = Bookmark(
        url="https://example.com",
        title="Example",
        description="An example bookmark",
    )
    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)

    result = get_bookmark(session, bookmark.id)

    assert result is bookmark
    assert result.id == bookmark.id
    assert result.url == "https://example.com"
    assert result.title == "Example"


def test_get_bookmark_raises_not_found(session):
    with pytest.raises(BookmarkNotFoundError):
        get_bookmark(session, 999)
