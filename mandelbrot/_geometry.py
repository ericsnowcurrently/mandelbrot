
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

    @property
    def imaginary(self):
        return self.x + self.y * 1j
