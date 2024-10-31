from typing import Any
import pygame as pg
import sys
sys.path.append('engine')
from config import WND_WIDTH, SIZE
from sprites import MonoSprite
from gun import Gun


SPEED: int = int(SIZE * .3)


class Model0(MonoSprite):
    def __init__(self,
                 image: pg.Surface,
                 pos: tuple[int, int],
                 sizes: tuple[int, int],
                 speed: int = SPEED,
                 shiftable: bool = True) -> None:
        super().__init__(image, pos, sizes, shiftable)
        self.speed: int = speed
        self.move_bounds: tuple[int, int] = 0, WND_WIDTH - sizes[0]

    def update(self) -> None:
        keys: pg.key.ScancodeWrapper = pg.key.get_pressed()
        self.key_move(keys)
        self.check_move()

    def key_move(self, keys: pg.key.ScancodeWrapper) -> None:
        if keys[pg.K_RIGHT]:
            speed: int = Model0.reflect(self.speed)
            self.rect.move_ip(speed, 0)
        if keys[pg.K_LEFT]:
            speed: int = Model0.reflect(self.speed, positive=False)
            self.rect.move_ip(speed, 0)

    def check_move(self) -> None:
        x: int = self.rect.left
        if x <= self.move_bounds[0]:
            speed: int = Model0.reflect(self.speed)
            self.rect.move_ip(speed, 0)
        if x >= self.move_bounds[1]:
            speed: int = Model0.reflect(self.speed, positive=False)
            self.rect.move_ip(speed, 0)

    @staticmethod
    def reflect(value: int, positive: bool = True) -> int:
        if value < 0 and positive:
            value *= -1
        if value > 0 and not positive:
            value *= -1
        return value


class SpaceShip(Model0):
    def __init__(self,
                 image: pg.Surface,
                 pos: tuple[int, int],
                 sizes: tuple[int, int],
                 shoot_mus: str,
                 speed: int = SPEED,
                 alive: bool = True,
                 shiftable: bool = True) -> None:
        super().__init__(image, pos, sizes, speed, shiftable)
        bullet_sizes: tuple[int, int] = int(SIZE * .5), SIZE
        self.gun: Gun = Gun(bullet_sizes, limited=False)
        self.alive: bool = alive
        self.sound: pg.mixer.Sound = pg.mixer.Sound(shoot_mus)

    def draw(self, wnd: pg.Surface) -> None:
        if self.alive:
            super().draw(wnd)

    def play(self, bullet_group: Any) -> None:
        """Method update, but shooting allowed"""
        if self.alive:
            keys: pg.key.ScancodeWrapper = pg.key.get_pressed()
            self.key_move(keys)
            self.key_shoot(keys, bullet_group)
            self.check_move()
    
    def key_shoot(self, keys: pg.key.ScancodeWrapper, 
                  bullet_group: Any) -> None:
        self.gun._recharge()
        if keys[pg.K_SPACE] and self.gun._charged:
            self.sound.play()
            self.gun.shoot(self, bullet_group)

    
