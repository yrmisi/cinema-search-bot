from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .movie import Movie


class SearchIDMovie(Base):
    __table_args__ = (
        UniqueConstraint(
            "chat_id",
            "search_id",
            "movie_id",
            name="unique_chat_search_movie",
        ),
    )
    chat_id: Mapped[int]
    search_id: Mapped[str]
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=True)
    page: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("page >= 1 AND page <= 10", name="check_page_range"),
    )

    movie: Mapped["Movie"] = relationship(
        "Movie",
        back_populates="searches",
        lazy="raise_on_sql",
    )
