from pathlib import Path
from environs import Env
from dataclasses import dataclass

env = Env()


@dataclass
class Config:
    PROJECT_DIR: Path = Path(__file__).parent.parent
    DEFAULT_MOVIES_CSV: Path = PROJECT_DIR / 'default_movie_list.csv'
    MOVIES_CSV: Path = env.path('MOVIES_CSV', default=DEFAULT_MOVIES_CSV)


config = Config()
