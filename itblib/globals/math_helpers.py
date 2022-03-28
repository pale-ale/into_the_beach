"""Contains some functions to calculate flight paths and other things."""

def get_parabola_half(point, peak):
    """
    Returns the points for a parabola passing through point, with it's peak at peak.
    The parabola always starts at (0,0) and moves to peak
    """
    dx = point[0] - peak[0]
    dy = point[1] - peak[1]
    a = dy/(dx**2)
    return lambda x: a*(x-peak[0])**2 + peak[1]

def get_parabola_full(peak, p_1, p_2):
    """
    Returns the points for two half-parabolas passing through p1, peak, then p2.
    """
    para_1 = get_parabola_half(p_1, peak)
    para_2 = get_parabola_half(p_2, peak)
    return lambda x: para_1(x) if x < peak[0] else para_2(x)

def get_parabola_time(peak, point_1, point_2):
    """
    Return a function returning the coordinates of a parabola according to a "time" parameter.
    The "time" param for the function is the travel time betweeen 0(start) and 1(end).
    """
    p1_x, p1_y = point_1
    p2_x, p2_y = point_2
    peak_x, peak_y = peak
    parabola = get_parabola_full((0.5, peak_y), (0, p1_y), (1, p2_y))
    linear = lambda x: p1_x + x*(p2_x - p1_x)
    return lambda time: (linear(time), parabola(time))
