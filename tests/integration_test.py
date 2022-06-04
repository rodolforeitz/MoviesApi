from pytest import mark
from pathlib import Path

from src.app import app
from src.config import config
from src.repositories import Database


@mark.parametrize('movies_csv_name', [
    'default_none_won.csv',
    'no_movies.csv',
    'one_won.csv',
    'two_same_producer_movies_one_won.csv'
])
def test_empty_response(resources_dir: Path, movies_csv_name: str) -> None:
    app.init(Database(movies_csv=resources_dir / movies_csv_name))
    test_client = app.test_client()

    response = test_client.open('/producers/winners/min_max_win_interval', method='GET')
    assert response.json == {
        'max': [], 'min': []
    }


def test_two_wins_same_year(resources_dir: Path) -> None:
    app.init(Database(movies_csv=resources_dir / 'two_wins_same_year.csv'))
    test_client = app.test_client()

    response = test_client.open('/producers/winners/min_max_win_interval', method='GET')
    assert response.json == {
        'max': [
            {
                'followingWin': 1980,
                'interval': 0,
                'previousWin': 1980,
                'producer': 'Producer 1'
            }
        ],
        'min': [
            {
                'followingWin': 1980,
                'interval': 0,
                'previousWin': 1980,
                'producer': 'Producer 1'
            }
        ]
    }


def test_producers_same_win_interval_max_min(resources_dir: Path) -> None:
    app.init(Database(movies_csv=resources_dir / 'producers_same_win_interval_max_min.csv'))
    test_client = app.test_client()

    response = test_client.open('/producers/winners/min_max_win_interval', method='GET')
    assert response.json == {
        'max': [
            {
                'followingWin': 1990,
                'interval': 10,
                'previousWin': 1980,
                'producer': 'Producer 1'
            },
            {
                'followingWin': 2000,
                'interval': 10,
                'previousWin': 1990,
                'producer': 'Producer 2'
            }
        ],
        'min': [
            {
                'followingWin': 1955,
                'interval': 5,
                'previousWin': 1950,
                'producer': 'Producer 3'
            },
            {
                'followingWin': 2005,
                'interval': 5,
                'previousWin': 2000,
                'producer': 'Producer 4'
            }
        ]
    }


def test_default_movies_csv() -> None:
    app.init(Database(movies_csv=config.DEFAULT_MOVIES_CSV))
    test_client = app.test_client()

    response = test_client.open('/producers/winners/min_max_win_interval', method='GET')
    assert response.json == {
        'max': [
            {
                'followingWin': 2015,
                'interval': 13,
                'previousWin': 2002,
                'producer': 'Matthew Vaughn'
            }
        ],
        'min': [
            {
                'followingWin': 1991,
                'interval': 1,
                'previousWin': 1990,
                'producer': 'Joel Silver'
            }
        ]
    }


def test_default_all_won(resources_dir: Path) -> None:
    app.init(Database(movies_csv=resources_dir / 'default_all_won.csv'))
    test_client = app.test_client()

    response = test_client.open('/producers/winners/min_max_win_interval', method='GET')
    print(response.json)
    assert response.json == {
        'max': [
            {
                'followingWin': 2016,
                'interval': 24,
                'previousWin': 1992,
                'producer': 'Charles Roven'
            }
        ],
        'min': [
            {
                'followingWin': 2007,
                'interval': 0,
                'previousWin': 2007,
                'producer': 'John Davis'
            },
            {
                'followingWin': 1985,
                'interval': 0,
                'previousWin': 1985,
                'producer': 'Irwin Winkler'
            },
            {
                'followingWin': 2001,
                'interval': 0,
                'previousWin': 2001,
                'producer': 'Elie Samaha'
            },
            {
                'followingWin': 2014,
                'interval': 0,
                'previousWin': 2014,
                'producer': 'Ian Bryce'
            },
            {
                'followingWin': 2009,
                'interval': 0,
                'previousWin': 2009,
                'producer': 'Lorenzo di Bonaventura'
            },
            {
                'followingWin': 2011,
                'interval': 0,
                'previousWin': 2011,
                'producer': 'Jack Giarraputo'
            },
            {
                'followingWin': 2015,
                'interval': 0,
                'previousWin': 2015,
                'producer': 'Adam Sandler'
            }
        ]
    }
