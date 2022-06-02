from dataclasses import asdict
from typing import Any, Optional
from flask import Flask, jsonify, Response

from src.config import config
from src.repositories import Database
from src.services import MoviesService


class App(Flask):
    def __init__(self: 'App', *args: list[Any], **kwargs: dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._database = None
        self._movies_service = None

    def init(self: 'App', database_: Database) -> None:
        self._database = database_
        self._movies_service = MoviesService(self._database.movies_repository)

    @property
    def movies_service(self: 'App') -> Optional[MoviesService]:
        return self._movies_service


app = App(__name__)


@app.route('/producers/winners/min_max_win_interval', methods=['GET'])
def get_min_max_win_interval() -> Response:
    min_max_win_interval = app.movies_service.find_min_max_win_interval()
    response = asdict(min_max_win_interval)
    return jsonify(response)


def main() -> None:
    app.init(Database(movies_csv=config.MOVIES_CSV))
    app.run()


if __name__ == '__main__':
    main()
