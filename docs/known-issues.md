# Known issues — kept as learning artefacts

## Integration test pollutes the file database

`tests/test_bookmarks.py::test_create_and_get_bookmark` inserts a bookmark
with `url="https://example.com"` into the production `bookmarks.db` file.
On subsequent runs the duplicate detection (correctly) raises
`DuplicateBookmarkError` and the test fails with `409 != 201`.

This is a test design issue, not a code issue. The fix is to use an
in-memory SQLite session per test, as `tests/test_bookmark_service.py`
already does for unit tests.

Deferred deliberately so the class can discuss test isolation patterns.
