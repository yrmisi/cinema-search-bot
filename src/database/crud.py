from dataclasses import asdict

from sqlalchemy import inspect, select
from sqlalchemy.orm import selectinload

from logging_config import get_logger
from utils import MovieInfo

from .db_config import AsyncSessionLocal
from .models import Movie, SearchIDMovie

logger = get_logger(__name__)


def model_fields(
    data: dict[str, str | int | float],
    model_obj: type[Movie] | type[SearchIDMovie],
) -> dict[str, str | int | float]:
    """Filters SQLAlchemy model fields."""
    logger.info("We get the fields specified in the models and filter the resulting dictionary by them.")
    obj_fields: set[str] = set(inspect(model_obj).columns.keys())
    return {key: val for key, val in data.items() if key in obj_fields}


async def create_movie_db(movies_data: MovieInfo | list[MovieInfo]) -> Movie:
    """Record is being created in the database."""
    if isinstance(movies_data, list):
        logger.info("Initialize the MovieInfo object list into the Movie and SearchIDMovie models")
        movies: list[Movie] = [Movie(**model_fields(asdict(data), Movie)) for data in movies_data]
        search_id_movie: list[SearchIDMovie] = [
            SearchIDMovie(**model_fields(asdict(data), SearchIDMovie)) for data in movies_data
        ]
    else:
        logger.info("Initialize the MovieInfo object into the Movie and SearchIDMovie models")
        movies = [Movie(**model_fields(asdict(movies_data), Movie))]
        search_id_movie = [SearchIDMovie(**model_fields(asdict(movies_data), SearchIDMovie))]

    async with AsyncSessionLocal() as async_session:
        async_session.add_all(movies)
        await async_session.flush()
        logger.info("Writing to the 'movies' table was successful.")

        for idx, search in enumerate(search_id_movie):
            search.movie_id = movies[idx].id

        async_session.add_all(search_id_movie)
        await async_session.commit()
        logger.info("Writing to the 'searchidmovies' table was successful.")

        return movies[0]


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
