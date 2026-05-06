from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.routers import bookmarks, tags, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Bookmark Manager",
    description="A small bookmark service used as a Claude Code config sandbox.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
