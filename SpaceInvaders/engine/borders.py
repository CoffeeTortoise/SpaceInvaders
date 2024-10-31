import pygame as pg
import sys
sys.path.append('engine')
from shapes import RectangleShape, CircleShape
from colors import YELLOW


class RectangleBorder(RectangleShape):  
    def __init__(self,
                 sizes: tuple[int, int],
                 pos: tuple[int, int],
                 line_width: int = 1,
                 color: tuple[int, int, int] = YELLOW) -> None:
        super().__init__(sizes, pos, color)
        self.line_width: int = line_width

    def draw(self, wnd: pg.Surface) -> None:
        pg.draw.rect(wnd, self.color, self.rect, self.line_width)


class CircleBorder(CircleShape):
    def __init__(self,
                 radius: int,
                 center: tuple[int, int],
                 line_width: int = 1,
                 color: tuple[int, int, int] = YELLOW) -> None:
        super().__init__(radius, center, color)
        self.line_width: int = line_width

    def draw(self, wnd: pg.Surface) -> None:
        pg.draw.circle(wnd, self.color, self.center, self.radius, self.line_width)
    
