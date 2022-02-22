"""Simple vector math methods"""

from math import atan2, cos, degrees, sin
from typing import Tuple, Union

Number = Union[float,int]
Vector = Tuple[Number, ...]
Vector2 = Tuple[Number, Number]
Matrix = Tuple[Vector, ...]

def mult2(a:Vector,b:Vector):
    """Multiply a*b component-wise, i.e (a0*b0, a1*b1)"""
    return a[0]*b[0], a[1]*b[1]

def smult(scalar:Number, vals:Vector) -> Vector:
    """Multiply a*b component-wise, i.e (a*b0, a*b1)"""
    return tuple([scalar*b for b in vals])

def add(*vectors:Vector2) -> Vector2:
    """Add a+b+... component-wise, i.e (a0+b0, a1+b1)"""
    assert len(vectors) >= 1, "Cannot add less than 1 vectors"
    x:Number = 0
    y:Number = 0
    for vector in vectors:
        x += vector[0]
        y += vector[1]
    return x,y

def sub(a:Vector2,b:Vector2) -> Vector2:
    """Subtract a-b component-wise, i.e (a0-b0, a1-b1)"""
    return a[0]-b[0], a[1]-b[1]

def deg_to_coord(x:float) -> tuple[int,int]:
    """@return: The vector with angle x in radians from the x axis CCW, length=1"""
    return cos(x), sin(x)

def vector_between(a:Vector2,b:Vector2,x:Vector2,s:float=1e-1) -> bool:
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

def transform_vector(m:Matrix,v:Vector) -> Vector:
    """Transform a vector v through a matrix m."""
    l = len(v)
    assert len(m) == l, "Matrix x-size must be equal to len(v)"
    for h in m:
        assert len(h) == l, "Every col-vector in m must be equal to len(v)"
    transformed:list[Number] = [0]*l
    for i, v_scalar in enumerate(v):
        for j, m_scalar in enumerate(m[i]):
            transformed[j] += m_scalar*v_scalar
    return tuple(transformed)
