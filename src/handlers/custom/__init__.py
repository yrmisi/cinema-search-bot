from .paginate_movies import router as paginate_router
from .random_movie import router as random_router
from .search_name import router as search_router

__all__ = [
    "search_router",
    "random_router",
    "paginate_router",
]
