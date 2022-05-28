"""Simple vector math methods"""

from math import cos, sin
from typing import Union

from pygame.math import Vector2 as FVector2

from multipledispatch import dispatch

Number = Union[int,float]
Vector = Union["IVector2", FVector2, tuple[Number, Number]]

class IVector2():
    _x: int
    _y: int

    @dispatch((object, FVector2, tuple))
    def __init__(self, vector: Vector):
        x, y = vector
        assert isinstance(x, int)
        assert isinstance(y, int)
        self._x, self._y = x, y

    @dispatch(int,int)
    def __init__(self, x:int, y:int):
        assert isinstance(x, int)
        assert isinstance(y, int)
        self._x, self._y = x, y
    
    @dispatch(int)
    def __init__(self, x:int):
        """
        The autocomplete hint is a lie. 
        Can be constructed with: int, (int,int), or another vector type
        """
        assert isinstance(x, int)
        self._x, self._y = x, x

    def __add__(self, vector: Vector):
        x,y = vector
        assert isinstance(x, int) or x.is_integer()
        assert isinstance(y, int) or y.is_integer()
        return IVector2(self.x + int(x), self.y + int(y))

    def __iter__(self):
        yield self._x
        yield self._y

    def __mul__(self, scalar):
        return IVector2(int(self.x * scalar), int(self.y * scalar))

    def __rmul__(self, scalar):
        return self * scalar

    def __sub__(self, vector: Vector):
        if isinstance(vector, tuple):
            x,y = vector
        else:
            x: "float|int" = vector.x
            y: "float|int" = vector.y
        assert isinstance(x, int) or x.is_integer()
        assert isinstance(y, int) or y.is_integer()
        return IVector2(self.x - int(x), self.y - int(y))
    
    def __eq__(self, other: Vector):
        other = IVector2(other)
        return self.c == other.c
    
    def __hash__(self):
        return hash(self.c)
    
    def __str__(self):
        return f"x:{self.x}, y:{self.y}"

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
   
    @property
    def c(self):
        """Return this IVector2 as tuple."""
        return self._x, self._y

    @x.setter
    def x(self, x: int):
        assert isinstance(x, int)
        self._x = x

    @y.setter
    def y(self, y: int):
        assert isinstance(y, int)
        self._y = y


def deg_to_coord(x: float):
    """@return: The vector with angle x in radians from the x axis CCW, length=1"""
    return FVector2(cos(x), sin(x))


def vector_between(a, b, x, s: float = 1e-1) -> bool:
    """
    Calculate whether a vector is between two other vectors.
    The "between" portion is chosen such that the angle between a and b is minimal.
    Undefined for an angle of pi/2, i.e. when a and b are opposite to one another.
    @a: first boundary
    @b: second boundary
    @x: vector to check
    @s: slack for float comparison
    @return: whether vector x is in between vectors a and b.
    """
    ax, ay = a
    bx, by = b
    xx, xy = x
    cprod_ax = ax*xy - ay*xx
    cprod_bx = bx*xy - by*xx
    cprod_ab = ax*by - ay*bx
    return cprod_ab * cprod_ax >= -s and cprod_ab * cprod_bx <= s


def transform_vector(m, v):
    """Transform a vector v through a matrix m."""
    l = len(v)
    assert len(m) == l, "Matrix x-size must be equal to len(v)"
    for h in m:
        assert len(h) == l, "Every col-vector in m must be equal to len(v)"
    transformed: list = [0]*l
    for i, v_scalar in enumerate(v):
        for j, m_scalar in enumerate(m[i]):
            transformed[j] += m_scalar*v_scalar
    return tuple(transformed)


def get_translation_for_center(a_pos, a_size, b_pos, b_size, horizontal=True, vertical=True):
    """Returns the amount a has to move by to be centered in relation to b."""
    ax, ay = a_pos
    adx, ady = a_size
    bx, by = b_pos
    bdx, bdy = b_size
    x = bx - ax + (bdx - adx)/2 if horizontal else 0
    y = by - ay + (bdy - ady)/2 if vertical else 0
    return (int(x),int(y))
