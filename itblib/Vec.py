"""Simple vector math methods"""

from typing import Sequence, Union
from math import sin, cos

number = Union[float,int]

def mult2(a:tuple[number,number],b:tuple[number,number]):
    """Multiply a*b component-wise, i.e (a0*b0, a1*b1)"""
    return (a[0]*b[0], a[1]*b[1])

def smult(scalar:number, vals:tuple[number]) -> tuple[number]:
    """Multiply a*b component-wise, i.e (a*b0, a*b1)"""
    return tuple([scalar*b for b in vals])

def add(*vals:tuple[number,number]) -> tuple[number,number]:
    """Add a+b+... component-wise, i.e (a0+b0, a1+b1)"""
    first = 0
    second = 0
    for x,y in vals:
        first += x
        second += y
    return (first,second)

def sub(a:tuple[number,number],b:tuple[number,number]) -> tuple[number,number]:
    """Subtract a-b component-wise, i.e (a0-b0, a1-b1)"""
    return (a[0]-b[0], a[1]-b[1])

def deg_to_coord(x:float) -> tuple[int,int]:
    """@return: The vector with angle x in radians from the x axis CCW, length=1"""
    return cos(x), sin(x)
    