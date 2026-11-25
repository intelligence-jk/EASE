from fractions import Fraction as F

import pytest

from motioncurves import CURVES, bezier, sample, spring, table, to_css, to_js
from motioncurves.__main__ import main


def test_hand_checked_values():
    assert CURVES["ease-in-quad"](F(1, 2)) == F(1, 4)
    assert CURVES["ease-out-quad"](F(1, 2)) == F(3, 4)
    assert CURVES["smoothstep"](F(1, 2)) == F(1, 2)
    assert CURVES["smoothstep"](F(1, 4)) == F(5, 32)  # (1/16)(3 - 1/2) = 5/32
    assert CURVES["ease-in-out-cubic"](F(1, 4)) == F(1, 16)
    assert CURVES["ease-in-out-cubic"](F(3, 4)) == F(15, 16)
    assert CURVES["smootherstep"](F(1, 2)) == F(1, 2)


@pytest.mark.parametrize("name", list(CURVES))
def test_ends_and_monotone(name):
    c = CURVES[name]
    assert c(0) == 0 and c(1) == 1
    vals = sample(c, 25)
    assert all(b >= a for a, b in zip(vals, vals[1:]))


@pytest.mark.parametrize("name", ["smoothstep", "smootherstep", "ease-in-out-cubic"])
def test_symmetry(name):
    c = CURVES[name]
    for i in range(0, 9):
        t = F(i, 8)
        assert c(t) + c(1 - t) == 1


def test_out_of_range():
    with pytest.raises(ValueError):
        CURVES["linear"](F(3, 2))
    with pytest.raises(ValueError):
        sample(CURVES["linear"], 1)
    with pytest.raises(ValueError):
        bezier(2, 0, 0.5, 1)


def test_bezier_matches_linear_and_ease_in_quad():
    lin = bezier(1 / 3, 1 / 3, 2 / 3, 2 / 3)
    for i in range(11):
        assert lin(F(i, 10)) == pytest.approx(i / 10, abs=1e-9)
    # the CSS ease-in curve starts slowly: at a tenth of the time it is under a tenth of the way
    c = bezier(0.42, 0, 1, 1)
    assert c(0) == pytest.approx(0) and c(1) == pytest.approx(1)
    assert c(F(1, 10)) < 0.1


def test_bezier_symmetric_ease():
    c = bezier(0.42, 0, 0.58, 1)
    assert c(F(1, 2)) == pytest.approx(0.5, abs=1e-9)


def test_spring_settles():
    s = spring()
    assert s(0) == pytest.approx(0)
    assert s(1) == 1.0
    assert abs(s(F(19, 20)) - 1) < 0.3


def test_exports_and_cli(capsys):
    assert to_css(0.42, 0, 0.58, 1) == "cubic-bezier(0.42, 0, 0.58, 1)"
    assert to_js(CURVES["linear"], 3, "my-curve") == "const my_curve = [0.00000, 0.50000, 1.00000];"
    assert table(CURVES["linear"], 2, "x").splitlines()[0] == "x: 2 frames"
    assert main(["table", "smoothstep", "5"]) == 0
    assert "frame   2  t=0.5000  value=0.5000" in capsys.readouterr().out
    assert main(["nope"]) == 2
