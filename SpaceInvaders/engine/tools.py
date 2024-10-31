from typing import Any
from time import perf_counter


class SaveLoad:

    @staticmethod
    def save(path: str, value: Any) -> None:
        item: str = str(value)
        with open(path, 'w') as file:
            file.write(item)

    @staticmethod
    def load(path: str) -> str:
        with open(path, 'r') as file:
            value: str = file.read()
        return value


class Timer:
    """A class for storing time intervals between cycles, secs"""
    def __init__(self) -> None:
        self.__last: bool = True
        self.__buffer: float = 0
        self.__last_time: float = 0

    def get_time(self) -> float:
        """Returns time in time buffer, secs"""
        if self.__last:
            self.__last_time = perf_counter()
            self.__last = False
        else:
            current_time: float = perf_counter()
            delta_time: float = current_time - self.__last_time
            self.__buffer += delta_time
            self.__last = True
        return self.__buffer

    def restart(self) -> None:
        """Clears the time buffer"""
        if self.__last:
            self.__buffer = 0
            self.__last_time = 0

    @property
    def buffer(self) -> float:
        """Time in time buffer, secs"""
        return self.__buffer

