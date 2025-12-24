from dataclasses import dataclass

from database.models import Movie


@dataclass
class MovieSearchResult:
    movie: Movie
    total_pages: int
