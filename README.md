# motion-curves

Easing curves for animation, written as plain maths you can check, with tables and exports for Manim, Remotion or CSS.

## What it solves
When you animate a number (a label sliding in, a bar growing, a camera pushing in), the curve decides how it feels. Most tools give you a name and hide the formula. Here every curve is a formula from 0 to 1 that starts at 0, ends at 1 and can be sampled at the exact frames of your video. The polynomial curves use exact `Fraction` arithmetic, so the values in the tests are hand-checkable. Pure Python 3.10+, standard library only.

## Example
```bash
python -m motioncurves table smoothstep 5
python -m motioncurves js ease-in-out-cubic 5
```
```
smoothstep: 5 frames
frame   0  t=0.0000  value=0.0000
frame   1  t=0.2500  value=0.1562
frame   2  t=0.5000  value=0.5000
frame   3  t=0.7500  value=0.8438
frame   4  t=1.0000  value=1.0000
const ease_in_out_cubic = [0.00000, 0.06250, 0.50000, 0.93750, 1.00000];
```
In Python:
```python
from fractions import Fraction as F
from motioncurves import CURVES, bezier
CURVES["smoothstep"](F(1, 4))      # Fraction(5, 32)
bezier(0.42, 0, 0.58, 1)(0.5)      # 0.5 (the CSS ease-in-out curve)
```

## The maths behind it
Smoothstep is f(t) = 3t^2 - 2t^3. At t = 1/4 that is 3/16 - 2/64 = 6/32 - 1/32 = 5/32, which is 0.15625, the 0.1562 above. Its slope is f'(t) = 6t - 6t^2, which is 0 at t = 0 and t = 1, so motion starts and stops gently. Smootherstep, 6t^5 - 15t^4 + 10t^3, also has zero acceleration at both ends. The cubic ease-in-out is 4t^3 for t below 1/2 and 1 - (2 - 2t)^3 / 2 after it, so at t = 1/4 it is 4/64 = 1/16 and at t = 3/4 it is 15/16. All three satisfy f(t) + f(1 - t) = 1, so the second half is the first half turned around, and the tests check this exactly.

A CSS style `cubic-bezier(x1, y1, x2, y2)` is a curve (x(s), y(s)) with x(s) = 3 x1 (1-s)^2 s + 3 x2 (1-s) s^2 + s^3 and the same for y. To find y at time t, the code solves x(s) = t by bisection (x is increasing when x1 and x2 are in [0, 1]) and returns y(s). The spring curve is 1 - e^(-kt) cos(2 pi n t), snapped to 1 at the end.

## Install and run
```bash
python -m pip install -e .
python -m motioncurves list
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
