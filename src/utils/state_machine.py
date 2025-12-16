from aiogram.fsm.state import State, StatesGroup


class SearchMovieNameState(StatesGroup):
    """State machine movie search by name"""

    name = State()
