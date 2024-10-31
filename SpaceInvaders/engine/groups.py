from typing import Any
import pygame as pg
import sys
sys.path.append('engine')
from bullet import BulletRectangle
from interfaces import Bullet
from monster import Alien


class Group:
    """Just class for grouping enitities"""
    def __init__(self) -> None:
        self._group: list[Any] = []

    def __getitem__(self, index: int) -> Any:
        return self._group[index]

    def __setitem__(self, index: int, item: Any) -> None:
        self._group[index] = item

    def __len__(self) -> int:
        return len(self._group)

    @property
    def group(self) -> list[Any]:
        return self._group


class BulletGroup(Group):
    """Class for grouping bullets.
    Has methods: all, draws, updates"""
    def __init__(self) -> None:
        super().__init__()
        self._group: list[Bullet] = []

    def all(self, wnd: pg.Surface) -> None:
        """Combination of draws and updates methods"""
        if len(self._group) == 0:
            return
        [item.draw(wnd) for item in self._group]
        [item.update() for item in self._group]

    def draws(self, wnd: pg.Surface) -> None:
        """Blitting object of that group on a window"""
        if len(self._group) == 0:
            return
        [item.draw(wnd) for item in self._group]

    def updates(self) -> None:
        """Calls update method of objects in that group"""
        if len(self._group) == 0:
            return
        [item.update() for item in self._group]


class AlienGroup(Group):
    """Class for grouping aliens.
    Has methods: draws, updates, interacts, kills_player"""
    def __init__(self) -> None:
        self._group: list[Alien] = []

    def draws(self, wnd: pg.Surface) -> None:
        """Blitting object of that group on a window"""
        if len(self._group) == 0:
            return
        [item.draw(wnd) for item in self._group]

    def updates(self) -> None:
        """Calls update method of objects in that group"""
        if len(self._group) == 0:
            return
        [item.update() for item in self._group]

    def interacts(self, bullet: BulletRectangle) -> None:
        """Calls interact method for objects in that group"""
        if len(self._group) == 0:
            return
        [item.interact(bullet) for item in self._group]

    def kills_player(self, player: Any) -> None:
        """Calls kill_player method for objects in that group"""
        if len(self._group) == 0:
            return
        [item.kill_player(player) for item in self._group]
