from dataclasses import dataclass


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
