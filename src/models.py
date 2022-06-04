from dataclasses import dataclass
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, ColumnDefault, Table, ForeignKey

Base = declarative_base()

producer_movie_tb = Table(
    'producer_movie',
    Base.metadata,
    Column('producer_id', ForeignKey('producers.id'), primary_key=True),
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
)


class Producer(Base):
    __tablename__ = 'producers'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    movies = relationship('Movie', secondary=producer_movie_tb, back_populates='producers')


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    year = Column(Integer)
    studios = Column(String(256))
    winner = Column(Boolean, ColumnDefault(False))
    producers = relationship('Producer', secondary=producer_movie_tb, back_populates='movies')


@dataclass
class WinInterval:
    producer: str
    interval: int
    previousWin: int
    followingWin: int


@dataclass
class MinMaxWinInterval:
    min: list[WinInterval]
    max: list[WinInterval]
