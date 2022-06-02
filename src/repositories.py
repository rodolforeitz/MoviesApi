import pandas
import pandasql
from pathlib import Path
from pandas import DataFrame

from enum import Enum
from src.models import WinInterval


class MinMaxMode(Enum):
    MAX = 'MAX'
    MIN = 'MIN'


class MoviesRepository:
    def __init__(self: 'MoviesRepository', movies_csv: Path) -> None:
        self._tb = pandas.read_csv(movies_csv, sep=';', keep_default_na=False)  # type: DataFrame
        self._tb.winner = self._tb.winner.astype(bool)

    def find_win_interval(self: 'MoviesRepository', min_max_mode: MinMaxMode) -> list[WinInterval]:
        movies_tb = self._tb
        query = f'''
        WITH
            index_tb AS (
                SELECT ROW_NUMBER() OVER (ORDER BY movies_tb.producers, movies_tb.year ASC) AS row,
                    movies_tb.producers,
                    movies_tb.year
                FROM
                    movies_tb
                WHERE movies_tb.winner = TRUE
            ),
            interval_tb AS (
                SELECT
                    idx1.producers,
                    idx1.year AS previous_win,
                    idx2.year AS following_win,
                    {min_max_mode.value}(idx2.year - idx1.year) AS interval
                FROM
                    index_tb AS idx1
                        JOIN index_tb AS idx2 ON idx2.row = idx1.row + 1 AND idx2.producers = idx1.producers
                GROUP BY idx1.producers
            )
        SELECT
            interval_tb.producers AS producer,
            interval_tb.interval,
            interval_tb.previous_win AS previousWin,
            interval_tb.following_win AS followingWin
        FROM
            interval_tb
        WHERE interval_tb.interval = (SELECT
                                          {min_max_mode.value}(interval_tb.interval)
                                      FROM
                                          interval_tb)'''

        query_result = pandasql.sqldf(query, locals())

        result = []
        for _, row in query_result.iterrows():
            result.append(WinInterval(**row.to_dict()))

        return result


class Database:
    def __init__(self: 'Database', movies_csv: Path) -> None:
        self._movies_repository = MoviesRepository(movies_csv)

    @property
    def movies_repository(self: 'Database') -> MoviesRepository:
        return self._movies_repository
