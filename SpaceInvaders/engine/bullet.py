import pygame as pg
import sys
sys.path.append('engine')
from colors import RED
from tools import Timer
from config import SIZE
from interfaces import Bullet
from shapes import RectangleShape
from enumerations import MoveDirection


START_POS: tuple[int, int] = 0, 0
LIFE_TIME: float = 1
SPEED: int = SIZE


def reflect(value: int, positive: bool = True) -> int:
    if value > 0 and not positive:
        value *= -1
    if value < 0 and positive:
        value *= -1
    return value


class BulletRectangle(Bullet):
    def __init__(self,
                 sizes: tuple[int, int],
                 speed: int = SPEED,
                 move_to: int = MoveDirection.UP,
                 life_time: float = LIFE_TIME,
                 exists: bool = True,
                 start_pos: tuple[int, int] = START_POS,
                 color: tuple[int, int, int] = RED) -> None:
        self.__bullet: RectangleShape = RectangleShape(sizes, start_pos, color)
        self.__timer: Timer = Timer()
        self.__life_time: float = life_time
        self._speed: int = speed
        self.move_to: int = move_to
        self.exists: bool = exists

    def draw(self, wnd: pg.Surface) -> None:
        if self.exists:
            self.__bullet.draw(wnd)

    def update(self) -> None:
        if self.exists:
            self._move_bullet()
            self._control_life()

    def _control_life(self) -> None:
        time: float = self.__timer.get_time()
        if time >= self.__life_time:
            self.exists = False

    def _move_bullet(self) -> None:
        if (self.move_to == MoveDirection.RIGHT) or (self.move_to == MoveDirection.DOWN):
            speed: int = reflect(self._speed)
        else:
            speed: int = reflect(self._speed, positive=False)
        if (self.move_to == MoveDirection.RIGHT) or (self.move_to == MoveDirection.LEFT):
            self.__bullet.rect.move_ip(speed, 0)
        else:
            self.__bullet.rect.move_ip(0, speed)


    @property
    def timer(self) -> Timer:
        return self.__timer

    @property
    def life_time(self) -> float:
        return self.__life_time

    @property
    def my_rect(self) -> pg.rect.Rect:
        return self.__bullet.rect

    @property
    def pos(self) -> tuple[int, int]:
        return self.__bullet.rect.left, self.__bullet.rect.top

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        c_pos: tuple[int, int] = self.__bullet.rect.left, self.__bullet.rect.top
        if pos != c_pos:
            self.__bullet.rect.left, self.__bullet.rect.top = pos

    @property
    def sizes(self) -> tuple[int, int]:
        return self.__bullet.rect.width, self.__bullet.rect.height

    @sizes.setter
    def sizes(self, sizes: tuple[int, int]) -> None:
        c_sizes: tuple[int, int] = self.__bullet.rect.width, self.__bullet.rect.height
        if sizes != c_sizes:
            self.__bullet.rect.width, self.__bullet.rect.height = sizes

