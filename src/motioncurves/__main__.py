"""python -m motioncurves list | table NAME FRAMES | js NAME FRAMES | css X1 Y1 X2 Y2"""
import sys

from .core import CURVES, table, to_css, to_js


def main(argv=None) -> int:
    a = sys.argv[1:] if argv is None else argv
    if a[:1] == ["list"]:
        print("\n".join(CURVES))
        return 0
    if a[:1] in (["table"], ["js"]) and len(a) == 3 and a[1] in CURVES and a[2].isdigit():
        fn = table if a[0] == "table" else to_js
        print(fn(CURVES[a[1]], int(a[2]), a[1]))
        return 0
    if a[:1] == ["css"] and len(a) == 5:
        print(to_css(*a[1:]))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
