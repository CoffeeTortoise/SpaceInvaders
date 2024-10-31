from enum import IntEnum


class ButtonState(IntEnum):
    """Just states of the button: inactive = 0, on hover = 1, active = 2"""
    INACTIVE = 0
    ON_HOVER = 1
    ACTIVE = 2


class MousePressed(IntEnum):
    """Mouse clicks: released = 0, left = 1, right = 2"""
    RELEASED = 0
    LEFT = 1
    RIGHT = 2


class MoveDirection(IntEnum):
    """Directions of movement: right = 0, left = 1, up = 2, down = 3"""
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class BulletType(IntEnum):
    """Types of bullets: rectangle = 0, circle = 1, sprite = 2"""
    RECTANGLE = 0
    CIRCLE = 1
    SPRITE = 2
