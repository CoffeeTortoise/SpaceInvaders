import pygame as pg
import sys
sys.path.append('engine')
from text import Text, FNT_SIZE
from borders import RectangleBorder
from colors import WHITE, BLACK, YELLOW
from enumerations import ButtonState, MousePressed


class Button(Text):
    def __init__(self,
                 text: str,
                 fnt_path: str,
                 pos: tuple[int, int],
                 fnt_size: int = FNT_SIZE,
                 border_width: int = 1,
                 fnt_color: tuple[int, int, int] = WHITE,
                 border_color: tuple[int, int, int] = YELLOW,
                 fill_color: tuple[int, int, int] | None = BLACK) -> None:
        super().__init__(text, fnt_path, pos, fnt_size, fnt_color, fill_color)
        border_sizes: tuple[int, int] = self._rect.width, self._rect.height
        self.__border: RectangleBorder = RectangleBorder(border_sizes, pos, border_width, border_color)
        self._state: int = ButtonState.INACTIVE
        self.mouse: int = MousePressed.RELEASED

    def draw(self, wnd: pg.Surface) -> None:
        wnd.blit(self._txt, self._rect)
        if self._state == ButtonState.ON_HOVER:
            self.__border.draw(wnd)

    def update(self) -> None:
        mouse_pos: tuple[int, int] = pg.mouse.get_pos()
        self._change_state(mouse_pos)
        if self._state == ButtonState.ON_HOVER:
            mouse_pressed: tuple[bool, ...] = pg.mouse.get_pressed()
            self._change_mouse(mouse_pressed)

    def _change_state(self, mouse_pos: tuple[int, int]) -> None:
        self._state = ButtonState.INACTIVE
        if self._rect.collidepoint(mouse_pos):
            self._state = ButtonState.ON_HOVER

    def _change_mouse(self, mouse_pressed: tuple[bool, ...]) -> None:
        self.mouse = MousePressed.RELEASED
        if mouse_pressed[0]:
            self.mouse = MousePressed.LEFT
        if mouse_pressed[2]:
            self.mouse = MousePressed.RIGHT
        if self.mouse != MousePressed.RELEASED:
            self._state = ButtonState.ACTIVE

