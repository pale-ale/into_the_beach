class Vec:
    """Simple vector math methods"""

    def comp_mult2(a:"tuple[float,float]",b:"tuple[float,float]"):
        """Multiply a*b component-wise, i.e (a0*b0, a1*b1)"""
        return (a[0]*b[0], a[1]*b[1])
    
    def comp_add2(a:"tuple[float,float]",b:"tuple[float,float]"):
        """Add a+b component-wise, i.e (a0+b0, a1+b1)"""
        return (a[0]+b[0], a[1]+b[1])

