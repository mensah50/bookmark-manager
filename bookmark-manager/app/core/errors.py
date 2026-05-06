class BookmarkError(Exception):
    """Base exception for bookmark domain errors."""


class BookmarkNotFoundError(BookmarkError):
    pass


class DuplicateBookmarkError(BookmarkError):
    pass


class InvalidURLError(BookmarkError):
    pass
