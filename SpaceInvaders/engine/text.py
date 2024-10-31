import sys
import pygame as pg
sys.path.append('engine')
from config import SIZE
from colors import WHITE, BLACK
from interfaces import PseudoSurface


FNT_SIZE: int = int(1.5 * SIZE)


class Text(PseudoSurface):
    """A class for flexible text management from pygame. Implemetns PseudoSurface interface. 
    Has methods: draw, change_text, change_fnt, change_fnt_color, change_fill_color, change_size.
    Has properties: sizes, pos
    """
    def __init__(self,
                 text: str,
                 fnt_path: str,
                 pos: tuple[int, int],
                 fnt_size: int = FNT_SIZE,
                 fnt_color: tuple[int, int, int] = WHITE,
                 fill_color: tuple[int, int, int] | None = BLACK) -> None:
        self.__text: str = text
        self.__fnt_path: str = fnt_path
        self.__fnt_size: int = fnt_size
        self.__fnt_color: tuple[int, int, int] = fnt_color
        self.__fill_color: tuple[int, int, int] | None = fill_color
        self.__font: pg.font.Font = pg.font.Font(self.__fnt_path, self.__fnt_size)
        if fill_color is None:
            self._txt: pg.Surface = self.__font.render(self.__text, 1, self.__fnt_color)
        else:
            self._txt: pg.Surface = self.__font.render(self.__text, 1, self.__fnt_color, self.__fill_color)
        self._rect: pg.rect.Rect = self._txt.get_rect()
        self._rect.left, self._rect.top = pos

    def draw(self, wnd: pg.Surface) -> None:
        """Draws text on a window"""
        wnd.blit(self._txt, self._rect)

    def _rebuild_txt(self) -> None:
        """Completely rebuilds text"""
        if self.__fill_color is None:
            self._txt: pg.Surface = self.__font.render(self.__text, 1, self.__fnt_color)
        else:
            self._txt: pg.Surface = self.__font.render(self.__text, 1, self.__fnt_color, self.__fill_color)

    def _rebuild_rect(self) -> None:
        """Recreates text rectangle"""
        pos: tuple[int, int] = self._rect.left, self._rect.top
        self._rect: pg.rect.Rect = self._txt.get_rect()
        self._rect.left, self._rect.top = pos

    def change_text(self, text: str) -> None:
        """Changes the text"""
        if text != self.__text:
            self.__text = text
            self._rebuild_txt()
            self._rebuild_rect()

    def change_size(self, fnt_size: int) -> None:
        """Changes font size"""
        if fnt_size != self.__fnt_size:
            self.__fnt_size = fnt_size
            self.__font = pg.font.Font(self.__fnt_path, self.__fnt_size)
            self._rebuild_txt()
            self._rebuild_rect()

    def change_fnt(self, fnt_path: str) -> None:
        """Changes font"""
        if fnt_path != self.__fnt_path:
            self.__fnt_path = fnt_path
            self.__font = pg.font.Font(self.__fnt_path, self.__fnt_size)
            self._rebuild_txt()
            self._rebuild_rect()

    def change_fnt_color(self, fnt_color: tuple[int, int, int]) -> None:
        """Changes font color"""
        if fnt_color != self.__fnt_color:
            self.__fnt_color = fnt_color
            self._rebuild_txt()

    def change_fill_color(self, fill_color: tuple[int, int, int] | None) -> None:
        """Changes background color"""
        if fill_color != self.__fill_color:
            self.__fill_color = fill_color
            self._rebuild_txt()

    @property
    def pos(self) -> tuple[int, int]:
        """Left top corner of the text rectangle"""
        return self._rect.left, self._rect.top

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        self._rect.left, self._rect.top = pos

    @property
    def sizes(self) -> tuple[int, int]:
        """Width and height of the text rectangle. Only getter"""
        return self._rect.width, self._rect.height

    @property
    def fnt_render(self) -> pg.font.Font:
        """Font from pygame. Only getter"""
        return self.__font


class Counter(PseudoSurface):
    """Graphical counter. Consists of two objects of the Text class. Implements PseudoSurface interface.
    Adds method: change_value.
    Adds properties: text, counter."""
    def __init__(self,
                 fnt_path: str,
                 text: str = 'SCORES:',
                 fnt_size: int = FNT_SIZE,
                 start_value: int = 0,
                 pos: tuple[int, int] = (0, 0),
                 fnt_color: tuple[int, int, int] = WHITE,
                 fill_color: tuple[int, int, int] | None = BLACK) -> None:
        self.__text: Text = Text(text, fnt_path, pos, fnt_size, fnt_color, fill_color)
        value: str = str(start_value)
        counter_pos: tuple[int, int] = self.__text.pos[0] + self.__text.sizes[0], self.__text.pos[1]
        self.__counter: Text = Text(value, fnt_path, counter_pos, fnt_size, fnt_color, fill_color)

    def draw(self, wnd: pg.Surface) -> None:
        self.__text.draw(wnd)
        self.__counter.draw(wnd)

    def change_value(self, value: int) -> None:
        """Changes the value of the counter"""
        new_value: str = str(value)
        self.__counter.change_text(new_value)

    @property
    def text(self) -> Text:
        """Returns Text object of the text"""
        return self.__text

    @property
    def counter(self) -> Text:
        """Returns Text object of the counter"""
        return self.__counter

    @property
    def pos(self) -> tuple[int, int]:
        return self.__text.pos

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        self.__text.pos = pos
        self.__counter.pos = pos[0] + self.__text.sizes[0], pos[1]

    @property
    def sizes(self) -> tuple[int, int]:
        return self.__text.sizes[0] + self.__counter.sizes[0], self.__text.sizes[1]
