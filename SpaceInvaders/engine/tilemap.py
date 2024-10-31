import pygame as pg
import sys
sys.path.append('engine')
from config import SIZE, WND_SIZE, ROWS, COLS
from interfaces import PseudoSurface


BLOCK_SIZES: tuple[int, int] = SIZE, SIZE


class PhonePicture(PseudoSurface):
    def __init__(self,
                 image: pg.Surface,
                 pos: tuple[int, int],
                 block_sizes: tuple[int, int] = BLOCK_SIZES) -> None:
        self.surface: pg.Surface = pg.surface.Surface(WND_SIZE)
        block_image: pg.Surface = pg.transform.scale(image, block_sizes)
        for i in range(ROWS):
            for j in range(COLS):
                block_pos: tuple[int, int] = SIZE * j, SIZE * i
                self.surface.blit(block_image, block_pos)
        self.rect: pg.rect.Rect = self.surface.get_rect()
        self.rect.left, self.rect.top = pos

    def draw(self, wnd: pg.Surface) -> None:
        wnd.blit(self.surface, self.rect)

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
            self.surface: pg.Surface = pg.transform.scale(self.surface, sizes)
            pos: tuple[int, int] = self.rect.left, self.rect.top
            self.rect: pg.rect.Rect = self.surface.get_rect()
            self.rect.left, self.rect.top = pos

