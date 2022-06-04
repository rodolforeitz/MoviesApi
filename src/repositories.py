import pandas
from pathlib import Path
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, Session

from enum import Enum
from src.models import Base, Producer, Movie, WinInterval


class MinMaxMode(Enum):
    MAX = 'MAX'
    MIN = 'MIN'


class ProducersRepository:

    @staticmethod
    def find_win_interval(db_session: Session, min_max_mode: MinMaxMode) -> list[WinInterval]:
        query = f'''
        WITH
            index_tb AS ( 
                SELECT ROW_NUMBER() OVER (ORDER BY producers.id, movies.year ASC) AS row,
                    producers.id AS producer_id,
                    producers.name AS producer,
                    movies.year AS movie_year
                FROM
                    producers AS producers
                        JOIN producer_movie AS pm ON producers.id = pm.producer_id
                        JOIN movies AS movies ON movies.id = pm.movie_id
                WHERE movies.winner = TRUE
            ),
            interval_tb AS (
                SELECT
                    idx1.producer_id,
                    idx1.producer,
                    idx1.movie_year AS previous_win,
                    idx2.movie_year AS following_win,
                    {min_max_mode.value}(idx2.movie_year - idx1.movie_year) AS interval
                FROM
                    index_tb AS idx1
                        JOIN index_tb AS idx2 ON idx2.row = idx1.row + 1 AND idx2.producer_id = idx1.producer_id
                GROUP BY idx1.producer_id
            )
        SELECT
            interval_tb.producer,
            interval_tb.interval,
            interval_tb.previous_win AS previousWin,
            interval_tb.following_win AS followingWin
        FROM
            interval_tb
        WHERE interval_tb.interval = (SELECT
                                          {min_max_mode.value}(interval_tb.interval)
                                      FROM
                                          interval_tb)'''

        query_result = db_session.execute(query)
        # noinspection PyProtectedMember
        result = [WinInterval(**row._mapping) for row in query_result]
        return result


class Database:
    def __init__(self: 'Database', movies_csv: Path) -> None:
        self._engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False},
                                     poolclass=StaticPool)
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()
        self._create_tables()
        self._populate_db(movies_csv)

    def _create_tables(self: 'Database') -> None:
        Base.metadata.create_all(self._engine)

    def _populate_db(self: 'Database', movies_csv: Path) -> None:
        movies_df = pandas.read_csv(movies_csv, sep=';', keep_default_na=False)  # type: DataFrame

        all_producers_by_name = {}
        movies = []
        for _, movie_row in movies_df.iterrows():
            producers_str = movie_row.producers.replace(' and ', ', ')  # type: str
            producers = []
            for producer_name in producers_str.split(','):
                producer_name = producer_name.strip()
                if len(producer_name) == 0:
                    continue
                if producer_name not in all_producers_by_name:
                    all_producers_by_name[producer_name] = Producer(name=producer_name)
                producers.append(all_producers_by_name[producer_name])

            winner = movie_row.winner == 'yes'
            movie = Movie(title=movie_row.title, year=movie_row.year, studios=movie_row.studios, winner=winner,
                          producers=producers)
            movies.append(movie)

        if len(movies) > 0:
            self._session.add_all(movies)
            self._session.flush()

    @property
    def session(self: 'Database') -> Session:
        return self._session
