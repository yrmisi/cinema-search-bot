from dataclasses import dataclass


@dataclass
class MovieInfo:
    poster_url: str
    description: str
    name: str
    movie_or_series: str
    duration: str
    budget: str
    rating_imdb: float
    rating_kp: float
    countries: str
    genres: str
    year: str
    chat_id: int
    search_id: str
    page: int
