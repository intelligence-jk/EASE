"""Easing curves: a function f from [0, 1] to progress, with f(0) = 0 and f(1) = 1.

Polynomial curves are evaluated with Fraction so tests can be exact.
"""
import math
from fractions import Fraction as F


def _as_fraction(t):
    t = F(t)
    if not 0 <= t <= 1:
        raise ValueError("t must be between 0 and 1")
    return t


def linear(t):
    return _as_fraction(t)


def ease_in_quad(t):
    t = _as_fraction(t)
    return t * t


def ease_out_quad(t):
    t = _as_fraction(t)
    return 1 - (1 - t) ** 2


def ease_in_out_cubic(t):
    t = _as_fraction(t)
    if t < F(1, 2):
        return 4 * t ** 3
    return 1 - (-2 * t + 2) ** 3 / 2


def smoothstep(t):
    t = _as_fraction(t)
    return t * t * (3 - 2 * t)


def smootherstep(t):
    t = _as_fraction(t)
    return t * t * t * (t * (6 * t - 15) + 10)


CURVES = {
    "linear": linear,
    "ease-in-quad": ease_in_quad,
    "ease-out-quad": ease_out_quad,
    "ease-in-out-cubic": ease_in_out_cubic,
    "smoothstep": smoothstep,
    "smootherstep": smootherstep,
}


def bezier(x1, y1, x2, y2):
    """CSS style cubic-bezier(x1, y1, x2, y2) as a function of time.

    Solves x(s) = t for s by bisection, then returns y(s). x1 and x2 must be in [0, 1]
    so that x(s) is increasing and the solution is unique.
    """
    if not (0 <= x1 <= 1 and 0 <= x2 <= 1):
        raise ValueError("x1 and x2 must be between 0 and 1")

    def coord(a, b, s):
        return 3 * a * (1 - s) ** 2 * s + 3 * b * (1 - s) * s ** 2 + s ** 3

    def f(t):
        t = float(_as_fraction(t))
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if coord(x1, x2, mid) < t:
                lo = mid
            else:
                hi = mid
        return coord(y1, y2, (lo + hi) / 2)

    return f


def spring(damping=0.5, cycles=2):
    """A decaying cosine that settles on 1: 1 - exp(-k t) cos(2 pi cycles t).

    The end is not exactly 1, so the value at t = 1 is snapped to 1.
    """
    k = 6 * (1 - damping) + 1

    def f(t):
        t = float(_as_fraction(t))
        if t == 1.0:
            return 1.0
        return 1 - math.exp(-k * t) * math.cos(2 * math.pi * cycles * t)

    return f


def sample(curve, frames):
    """Progress at each of `frames` frames, from frame 0 (value 0) to the last frame (value 1)."""
    if frames < 2:
        raise ValueError("need at least 2 frames")
    return [curve(F(i, frames - 1)) for i in range(frames)]


def table(curve, frames, name="curve"):
    rows = [f"{name}: {frames} frames"]
    for i, v in enumerate(sample(curve, frames)):
        rows.append(f"frame {i:3d}  t={float(F(i, frames - 1)):.4f}  value={float(v):.4f}")
    return "\n".join(rows)


def to_js(curve, frames, name="curve"):
    vals = ", ".join(f"{float(v):.5f}" for v in sample(curve, frames))
    return f"const {name.replace('-', '_')} = [{vals}];"


def to_css(x1, y1, x2, y2):
    return f"cubic-bezier({x1}, {y1}, {x2}, {y2})"
