from random import randint
from typing import Any
import pygame as pg
import sys
sys.path.append('engine')
from config import WND_WIDTH, WND_HEIGHT, SIZE
from bullet import BulletRectangle
from sprites import MonoSprite


SPEED: float = SIZE * .2
MAX_SPEED: float = SPEED * 7
UNUSED: tuple[int, int] = 0, 0


def reflect(value: float, positive: bool = True) -> float:
    if value > 0 and not positive:
        value *= -1
    if value < 0 and positive:
        value *= -1
    return value


class Alien(MonoSprite):
    amount: float = -.2
    counter: int = -1
    def __init__(self,
                 image: pg.Surface,
                 sizes: tuple[int, int],
                 shiftable: bool = True,
                 alive: bool = True,
                 speed: float = SPEED,
                 max_speed: float = MAX_SPEED,
                 pos: tuple[int, int] = UNUSED) -> None:
        super().__init__(image, pos, sizes, shiftable)
        Alien.amount += .2
        Alien.counter += 1
        self.speed: float = speed + Alien.amount
        if abs(self.speed) > abs(max_speed):
            self.speed = max_speed
        self.alive: bool = alive
        self.vertical: bool = False
        self.ground: int = self.rect.top + self.rect.width
        self.bounds_x: tuple[int, int] = 0, WND_WIDTH - self.rect.width 
        x: int = randint(self.bounds_x[0], self.bounds_x[1])
        alien_pos: tuple[int, int] = x, SIZE * 5
        self.rect.left, self.rect.top = alien_pos
        if Alien.counter % 2 == 0:
            self.to_right: bool = True
        else:
            self.to_right: bool = False

    def draw(self, wnd: pg.Surface) -> None:
        if self.alive:
            wnd.blit(self.image, self.rect)

    def update(self) -> None:
        if not self.alive:
            return
        if not self.vertical:
            self.horizontal_move()
        else:
            self.vertical_move()

    def interact(self, bullet: BulletRectangle) -> None:
        if (not self.alive) or (not bullet.exists):
            return
        if self.rect.colliderect(bullet.my_rect):
            self.alive = False
            bullet.exists = False

    def kill_player(self, player: Any) -> None:
        if (not self.alive) or (not player.alive):
            return
        if self.rect.colliderect(player.rect):
            self.alive = False
            player.alive = False

    def horizontal_move(self) -> None:
        if self.to_right:
            self.right_move()
        else:
            self.left_move()

    def right_move(self) -> None:
        x: int = self.rect.left
        if x >= self.bounds_x[1]:
            self.ground: int = self.rect.top + self.rect.width
            self.vertical = True
            self.to_right = False
        else:
            speed: float = reflect(self.speed)
            self.rect.move_ip(speed, 0)

    def left_move(self) -> None:
        x: int = self.rect.left
        if x <= self.bounds_x[0]:
            self.ground: int = self.rect.top + self.rect.width
            self.vertical = True
            self.to_right = True
        else:
            speed: float = reflect(self.speed, positive=False)
            self.rect.move_ip(speed, 0)

    def vertical_move(self) -> None:
        y: int = self.rect.top
        if y >= self.ground:
            self.vertical = False
        else:
            speed: float = reflect(self.speed)
            self.rect.move_ip(0, speed)
        self.check_y()

    def check_y(self) -> None:
        y: int = self.rect.top
        if y >= WND_HEIGHT:
            self.alive = False

    @staticmethod
    def back() -> None:
        """Changes values amount and counter to it's originall state"""
        Alien.amount = -.2
        Alien.counter = -1

