from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import BASE_DIR

DB_DIR: Path = BASE_DIR / "cinema_bot.db"
engine = create_async_engine(f"sqlite+aiosqlite:///{DB_DIR.as_posix()}")

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def on_shutdown():
    """Correct termination: closing the connection to the database."""
    await engine.dispose()
