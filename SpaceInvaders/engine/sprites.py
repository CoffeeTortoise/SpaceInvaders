import pygame as pg
import sys
sys.path.append('engine')
from interfaces import Sprite


class MonoSprite(Sprite):
    def __init__(self,
                 image: pg.Surface,
                 pos: tuple[int, int],
                 sizes: tuple[int, int],
                 shiftable: bool = True) -> None:
        self.image: pg.Surface = pg.transform.scale(image, sizes)
        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.shiftable: bool = shiftable

    def draw(self, wnd: pg.Surface) -> None:
        wnd.blit(self.image, self.rect)

    def update(self) -> None:
        print('Coming soon')

    def shift(self, dx: int = 0,
              dy: int = 0) -> None:
        if self.shiftable:
            self.rect.move_ip(dx, dy)

    @property
    def pos(self) -> tuple[int, int]:
        return self.rect.left, self.rect.top

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        if pos != (self.rect.left, self.rect.top):
            self.rect.left, self.rect.top = pos

    @property
    def sizes(self) -> tuple[int, int]:
        return self.rect.width, self.rect.height

    @sizes.setter
    def sizes(self, sizes: tuple[int, int]) -> None:
        if sizes != (self.rect.width, self.rect.height):
            self.image: pg.Surface = pg.transform.scale(self.image, sizes)
            pos: tuple[int, int] = self.rect.left, self.rect.top
            self.rect: pg.rect.Rect = self.image.get_rect()
            self.rect.left, self.rect.top = pos

    @property
    def my_rect(self) -> pg.rect.Rect:
        return self.rect

