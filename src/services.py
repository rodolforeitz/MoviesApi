from src.models import MinMaxWinInterval
from src.repositories import MoviesRepository, MinMaxMode


class MoviesService:
    def __init__(self: 'MoviesService', repository: MoviesRepository) -> None:
        self._repository = repository

    def find_min_max_win_interval(self: 'MoviesService') -> MinMaxWinInterval:
        min_win_interval = self._repository.find_win_interval(MinMaxMode.MIN)
        max_win_interval = self._repository.find_win_interval(MinMaxMode.MAX)
        return MinMaxWinInterval(min_win_interval, max_win_interval)
