import sys
import pygame as pg
sys.path.append('engine')
from interfaces import Shape
from colors import WHITE


class RectangleShape(Shape):
    """Implements the Shape interface for rectangle"""
    def __init__(self,
                 sizes: tuple[int, int],
                 pos: tuple[int, int],
                 color: tuple[int, int, int] = WHITE) -> None:
        self.rect: pg.rect.Rect = pg.rect.Rect(pos[0], pos[1], sizes[0], sizes[1])
        self.color: tuple[int, int, int] = color

    def draw(self, wnd: pg.Surface) -> None:
        pg.draw.rect(wnd, self.color, self.rect)

    def resize(self, sizes: tuple[int, int]) -> None:
        if sizes != (self.rect.width, self.rect.height):
            self.rect.width, self.rect.height = sizes

    def change_color(self, color: tuple[int, int, int]) -> None:
        if color != self.color:
            self.color = color

    @property
    def pos(self) -> tuple[int, int]:
        return self.rect.left, self.rect.top

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        self.rect.left, self.rect.top = pos

    @property
    def sizes(self) -> tuple[int, int]:
        return self.rect.width, self.rect.height


class CircleShape(Shape):
    """Implements the Shape interface for circle. Adds rect property"""
    def __init__(self,
                 radius: int,
                 center: tuple[int, int],
                 color: tuple[int, int, int] = WHITE) -> None:
        self.color: tuple[int, int, int] = color
        self.center: tuple[int, int] = center
        self.radius: int = radius

    def draw(self, wnd: pg.Surface) -> None:
        pg.draw.circle(wnd, self.color, self.center, self.radius)

    def resize(self, sizes: tuple[int, int]) -> None:
        """Changes the radius of the circle. So, sizes[0] must be equal to sizes[1]"""
        if sizes[0] != sizes[1]:
            return
        else:
            self.radius = sizes[0]

    def change_color(self, color: tuple[int, int, int]) -> None:
        if color != self.color:
            self.color = color

    @property
    def pos(self) -> tuple[int, int]:
        """Center of the circle"""
        return self.center

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        if pos != self.center:
            self.center = pos

    @property
    def sizes(self) -> tuple[int, int]:
        """Sizes of the corresponding rectangle"""
        size: int = self.radius * 2
        return size, size

    @property
    def rect(self) -> pg.rect.Rect:
        """Corresponding rectangle"""
        sizes: tuple[int, int] = self.radius * 2, self.radius * 2
        pos: tuple[int, int] = self.center[0] - self.radius, self.center[1] - self.radius
        return pg.rect.Rect(pos[0], pos[1], sizes[0], sizes[1])
