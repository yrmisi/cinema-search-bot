from sqlalchemy import select
from sqlalchemy.orm import selectinload

from logging_config import get_logger

from ..db_config import AsyncSessionLocal
from ..models import Movie, SearchIDMovie

logger = get_logger(__name__)


async def get_movie_db(chat_id: int, search_id: str, page: int) -> Movie | None:
    """We get a Movie object by chat ID, search ID and pages."""
    logger.info("Get movie object by ID")

    async with AsyncSessionLocal() as async_session:
        stmt = (
            select(SearchIDMovie)
            .where(
                SearchIDMovie.chat_id == chat_id,
                SearchIDMovie.search_id == search_id,
                SearchIDMovie.page == page,
            )
            .options(selectinload(SearchIDMovie.movie))
        )
        result = await async_session.execute(stmt)
        search = result.scalar_one_or_none()

        logger.info("Movie object received successfully")
        return search.movie if search else None
