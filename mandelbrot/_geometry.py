
import math

from ._util import as_namedtuple, Steps


class Grid:

    __slots__ = ('_width', '_height')

    def __new__(cls, width, height=None):
        width = Steps(width)
        height = Steps(height) if height is not None else width

        self = super().__new__(cls)
        self._width = width
        self._height = height
        return self

    def __len__(self):
        return len(self.width) * len(self.height)

    def __iter__(self):
        # Iterate up the rows, left to right.
        for j in self.height:
            for i in self.width:
                yield (i, j)

    def __reversed__(self):
        for j in reversed(self.height):
            for i in reversed(self.width):
                yield (i, j)

    def __contains__(self, value):
        try:
            x, y = value
        except (TypeError, ValueError):
            return False
        return x in self.width and y in self.height

    def __getitem__(self, index):
        if index not in self.height:
            raise IndexError(index)
        return self.width

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def iter_floats(self, xstart, xend, ystart, yend):
        for j in self.height.iter_floats(ystart, yend):
            for i in self.width.iter_floats(xstart, xend):
                yield (i, j)

    def iter_points(self, start, end):
        start = Point2D.from_raw(start)
        end = Point2D.from_raw(end)
        for i, j in self.iter_floats(start.x, end.x, start.y, end.y):
            yield Point2D(i, j)


@as_namedtuple('x y')
class Point2D:

    __slots__ = []

    @classmethod
    def from_raw(cls, raw):
        if raw is None:
            return None
        if isinstance(raw, Point2D):
            return raw
        if isinstance(raw, str):
            return cls.parse(raw)
        if isinstance(raw, (int, float)):
            # Assume it's a number in the complex plane.
            return cls(raw, 0)
        if isinstance(raw, complex):
            return cls(raw.real, raw.imag)

        try:
            x, y = raw
        except (TypeError, ValueError):
            raise ValueError('unsupported raw point {!r}'.format(raw))
        return cls(x, y)

    @classmethod
    def parse(cls, ptstr):
        try:
            if not isinstance(ptstr, str):
                raise ValueError('not a string')
            if not ptstr:
                return cls()

            # Strip the wrapping brackets, if any.
            if ptstr.startswith('('):
                if not ptstr.endswith(')'):
                    raise ValueError
                ptstr = ptstr[1: -1]
            elif ptstr.startswith('['):
                if not ptstr.endswith(']'):
                    raise ValueError
                ptstr = ptstr[1: -1]
            elif ptstr.endswith((')', ']')):
                raise ValueError

            # Extract the numbers.
            values = tuple(val.strip()
                           for val in ptstr.split(','))
            try:
                x, y = values
            except ValueError:
                if not ptstr.endswith(('i', 'j')):
                    raise ValueError(
                            'expected 2 numbers, got {}'.format(len(values)))
                c = complex(ptstr.replace('i', 'j'))
                x, y = c.real, c.imag

            # Create a Point2D with those numbers.
            try:
                self = cls(x, y)
            except ValueError:
                raise ValueError('must be floats')
        except ValueError as exc:
            msg = 'unsupported point string {!r}'.format(ptstr)
            if exc.args:
                msg += ' ({})'.format(exc)
            raise ValueError(msg)

        return self

    def __new__(cls, x=0.0, y=0.0, valuetype=float):
        # XXX Fraction or Decimal instead of float?
        if valuetype is not None:
            x = valuetype(x) if x is not None else None
            y = valuetype(y) if y is not None else None
        self = super().__new__(cls, x, y)
        return self

    def __init__(self, *args, **kwargs):
        # no super call

        if self.x is None:
            raise TypeError('missing x')

        if self.y is None:
            raise TypeError('missing y')

    def __str__(self):
        return '({}, {})'.format(*self)

    def _resolve_other(self, other):
        try:
            other_x, other_y = other
        except (TypeError, ValueError):
            try:
                other_x = other.x
                other_y = other.y
            except AttributeError:
                other_x = other_y = other
        return other_x, other_y

    def __add__(self, other):
        other_x, other_y = self._resolve_other(other)
        x = self.x + other_x
        y = self.y + other_y
        return self._replace(x=x, y=y)

    def __sub__(self, other):
        other_x, other_y = self._resolve_other(other)
        x = self.x - other_x
        y = self.y - other_y
        return self._replace(x=x, y=y)

    def __mul__(self, other):  # dot product
        other_x, other_y = self._resolve_other(other)
        x = self.x * other_x
        y = self.y * other_y
        return self._replace(x=x, y=y)

    def __truediv__(self, other):
        other_x, other_y = self._resolve_other(other)
        x = self.x / other_x
        y = self.y / other_y
        return self._replace(x=x, y=y)

    def __floordiv__(self, other):
        other_x, other_y = self._resolve_other(other)
        x = self.x // other_x
        y = self.y // other_y
        return self._replace(x=x, y=y)

    def __neg__(self):
        return self._replace(x=-self.x, y=-self.y)

    def __abs__(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

    def __invert__(self):
        return self._replace(x=self.y, y=self.x)

    def __complex__(self):
        return self.x + self.y * 1j

    def __round__(self, *args):
        return self._replace(x=round(self.x, *args), y=round(self.y, *args))

    def __ceil__(self):
        return self._replace(x=math.ceil(self.x), y=math.ceil(self.y))

    def __floor__(self):
        return self._replace(x=math.floor(self.x), y=math.floor(self.y))

    def __trunc__(self):
        return self._replace(x=math.trunc(self.x), y=math.trunc(self.y))

    @property
    def quadrance(self):
        return self.x * self.x + self.y * self.y


@as_namedtuple('min max')
class Area:

    __slots__ = []

    @classmethod
    def from_radius(cls, radius=None, center=None):
        radius = float(radius) if radius else 1
        if radius <= 0:
            raise ValueError('got non-positive radius')
        xcenter, ycenter = Point2D.from_raw(center) or Point2D()

        min = Point2D(xcenter - radius, ycenter - radius)
        max = Point2D(xcenter + radius, ycenter + radius)
        return cls(min, max)

    @classmethod
    def from_sides(cls, x1, x2, y1, y2):
        return cls((x1, x2), (y1, y2))

    def __new__(cls, p1, p2):
        p1 = Point2D.from_raw(p1)
        p2 = Point2D.from_raw(p2)
        pmin = Point2D(min(p1.x, p2.x), min(p1.y, p2.y))
        pmax = Point2D(max(p1.x, p2.x), max(p1.y, p2.y))
        self = super().__new__(cls, pmin, pmax)
        return self

    @property
    def delta(self):
        return self.max - self.min
