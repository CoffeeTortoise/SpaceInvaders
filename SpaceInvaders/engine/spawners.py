import pygame as pg
import sys
sys.path.append('engine')
from tools import Timer
from monster import Alien
from groups import AlienGroup


SPAWN_TIME: int = 2


class SpawnerAlien:
    def __init__(self,
                 image: pg.Surface,
                 sizes: tuple[int, int],
                 spawn_time: int = SPAWN_TIME) -> None:
        self._image: pg.Surface = image
        self._sizes: tuple[int, int] = sizes
        self._spawn_time: int = spawn_time
        self.__timer: Timer = Timer()

    def spawn(self, group: AlienGroup) -> None:
        time: float = self.__timer.get_time()
        if time >= self._spawn_time:
            alien: Alien = Alien(self._image, self._sizes)
            group.group.append(alien)
            self.__timer.restart()

    @property
    def timer(self) -> Timer:
        """Returns timer object of that spawner"""
        return self.__timer
