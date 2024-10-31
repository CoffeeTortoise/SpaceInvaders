from abc import ABC, abstractmethod
import pygame as pg
import sys
sys.path.append('engine')
from tools import Timer


# Entity interfaces

class Shape(ABC):

    @abstractmethod
    def draw(self, wnd: pg.Surface) -> None:
        """Method for blitting a shape on the screen"""
        pass

    @abstractmethod
    def resize(self, sizes: tuple[int, int]) -> None:
        """Method for resizing a shape"""
        pass

    @abstractmethod
    def change_color(self, color: tuple[int, int, int]) -> None:
        """Method for changing a color of the shape"""
        pass

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        """Returns the position of a shape(left top corner)"""
        pass

    @property
    @abstractmethod
    def sizes(self) -> tuple[int, int]:
        """Returns sizes of a shape(width, height)"""
        pass


class Sprite(ABC):

    @abstractmethod
    def draw(self, wnd: pg.Surface) -> None:
        """Method for blitting a sprite on the surface"""
        pass

    @abstractmethod
    def update(self) -> None:
        """Updates sprite state"""
        pass

    @abstractmethod
    def shift(self, dx: int = 0,
              dy: int = 0) -> None:
        """Shifts the sprite by dx and dy"""
        pass

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        """Left top corner of the sprite rect"""
        pass

    @property
    @abstractmethod
    def sizes(self) -> tuple[int, int]:
        """Width and height of the sprite rect"""
        pass

    @property
    @abstractmethod
    def my_rect(self) -> pg.rect.Rect:
        """Rectangle of that sprite"""
        pass


class PseudoSurface(ABC):

    @abstractmethod
    def draw(self, wnd: pg.Surface) -> None:
        """Draws that surface on another surface"""
        pass

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        """Left top corner of that surface"""
        pass

    @property
    @abstractmethod
    def sizes(self) -> tuple[int, int]:
        """Width and height of that surface"""
        pass


class Bullet(ABC):

    @abstractmethod
    def draw(self, wnd: pg.Surface) -> None:
        """Draws bullet on the screen"""
        pass

    @abstractmethod
    def update(self) -> None:
        """Updates bullet state"""
        pass

    @abstractmethod
    def _control_life(self) -> None:
        """Controls bullet lifetime"""
        pass

    @abstractmethod
    def _move_bullet(self) -> None:
        """Moves bullet according to chosen direction"""
        pass

    @property
    @abstractmethod
    def life_time(self) -> float:
        """Bullet lifetime, secs"""
        pass

    @property
    @abstractmethod
    def timer(self) -> Timer:
        """Timer object of that bullet"""
        pass

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        """Left top corner of the rectangle of that bullet"""
        pass

    @property
    @abstractmethod
    def sizes(self) -> tuple[int, int]:
        """Width and height of that bullet"""
        pass

    @property
    @abstractmethod
    def my_rect(self) -> pg.rect.Rect:
        """Rectangle of that bullet"""
        pass


# Group interfaces

