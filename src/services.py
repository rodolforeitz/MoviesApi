from sqlalchemy.orm import Session
from src.models import MinMaxWinInterval
from src.repositories import ProducersRepository, MinMaxMode


class ProducersService:
    @staticmethod
    def find_min_max_win_interval(db_session: Session) -> MinMaxWinInterval:
        min_win_interval = ProducersRepository.find_win_interval(db_session, MinMaxMode.MIN)
        max_win_interval = ProducersRepository.find_win_interval(db_session, MinMaxMode.MAX)
        return MinMaxWinInterval(min_win_interval, max_win_interval)
