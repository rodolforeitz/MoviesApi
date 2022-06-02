from pathlib import Path
from pytest import fixture

from src.config import config


@fixture
def resources_dir() -> Path:
    return config.PROJECT_DIR / 'tests' / 'resources'
