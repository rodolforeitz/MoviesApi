from typing import Any
from typing import Optional
from dataclasses import asdict
from sqlalchemy.orm import Session
from flask import Flask, jsonify, Response

from src.config import config
from src.repositories import Database
from src.services import ProducersService


class App(Flask):
    def __init__(self: 'App', *args: list[Any], **kwargs: dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._database = None  # type: Optional[Database]

    def init(self: 'App', database_: Database) -> None:
        self._database = database_

    @property
    def db_session(self: 'App') -> Session:
        return self._database.session


app = App(__name__)


@app.route('/producers/winners/min_max_win_interval', methods=['GET'])
def get_min_max_win_interval() -> Response:
    min_max_win_interval = ProducersService.find_min_max_win_interval(app.db_session)
    response = asdict(min_max_win_interval)
    return jsonify(response)


def main() -> None:
    app.init(Database(movies_csv=config.MOVIES_CSV))
    app.run()


if __name__ == '__main__':
    main()
