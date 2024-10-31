import sys
sys.path.append('engine')
from tools import Timer
from bullet import BulletRectangle
from enumerations import BulletType
from interfaces import Sprite
from groups import BulletGroup


CHARGE_TIME: float = .2
MAX_BULLETS: int = 10


class Gun:
    def __init__(self,
                 bullet_sizes: tuple[int, int],
                 limited: bool = True,
                 charged: bool = True,
                 charge_time: float = CHARGE_TIME,
                 bullets: int = MAX_BULLETS,
                 bullet_type: int = BulletType.RECTANGLE) -> None:
        self.__timer: Timer = Timer()
        self._charged: bool = charged
        self._charge_time: float = charge_time
        self._bullet_type: int = bullet_type
        self._bullet_sizes: tuple[int, int] = bullet_sizes
        self.limited: bool = limited
        self.bullets: int = bullets

    def shoot(self, shooter: Sprite,
              group: BulletGroup) -> None:
        self._recharge()
        if self._charged:
            self._control_limit()
            bullet: BulletRectangle = BulletRectangle(self._bullet_sizes)
            center: tuple[int, int] = shooter.my_rect.center
            bullet.my_rect.center = center
            self._charged = False
            group.group.append(bullet)

    def _recharge(self) -> None:
        if not self._charged:
            time: float = self.__timer.get_time()
            if time >= self._charge_time:
                self._charged = True
                self.__timer.restart()

    def _control_limit(self) -> None:
        if not self.limited:
            self.bullets = MAX_BULLETS

