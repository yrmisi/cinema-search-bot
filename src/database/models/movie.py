from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .search_id_movie import SearchIDMovie


class Movie(Base):
    poster_url: Mapped[str]
    description: Mapped[str]
    name: Mapped[str]
    movie_or_series: Mapped[str]
    duration: Mapped[str]
    budget: Mapped[str]
    rating_imdb: Mapped[float]
    rating_kp: Mapped[float]
    countries: Mapped[str]
    genres: Mapped[str]
    year: Mapped[int]

    searches: Mapped[list["SearchIDMovie"]] = relationship(
        "SearchIDMovie",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="raise_on_sql",
    )
