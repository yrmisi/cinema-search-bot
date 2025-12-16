from api import get_movies_data_by_api


class SearchMovieNameService:
    """ """

    @staticmethod
    def get_movies(movie_name: str):
        """ """
        query_data = {"query": movie_name}
        movies_data = get_movies_data_by_api(query_data)
        return "\n".join(movie["name"] for movie in movies_data)
