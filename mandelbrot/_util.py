
from collections import namedtuple
import functools


def as_namedtuple(cls, fields=None):
    if not fields and not isinstance(cls, type):
        # used as a decorator...
        fields = cls
        return lambda cls: as_namedtuple(cls, fields)

    if not isinstance(cls, type):
        raise ValueError('expected a class, got {!r}'.format(cls))
    if not fields:
        raise ValueError('expected fields, got none')

    nt = namedtuple(cls.__name__, fields)
    ns = {'__doc__': cls.__doc__,
          '__slots__': (),
          }
    if cls.__init__ is not object.__init__:
        _make = functools.wraps(nt._make)(lambda c, it: c(*it))
        ns['_make'] = classmethod(_make)
    sub = type(cls.__name__, (cls, nt), ns)
    return sub


# XXX steps as factor of 2?
# XXX factor as power of 2?


class Steps(int):

    __slots__ = ()

    def __new__(cls, num):
        if isinstance(num, Steps):
            return num
        self = super().__new__(cls, num)
        return self

    def __init__(self, *args, **kwargs):
        # validation
        if self < 0:
            raise TypeError(
                    'steps must be non-negative, got {}'.format(int(self)))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, int(self))

    def __len__(self):
        return 1 + self

    def __iter__(self):
        yield from range(len(self))

    def __reversed__(self):
        yield from range(self, -1, -1)

    def __contains__(self, value):
        try:
            if value < 0:
                return False
        except TypeError:  # unorderable, etc.
            return False
        return value <= self and isinstance(value, int)

    def range(self, start=None, stop=None, step=None):
        if start is None:
            if stop is None:
                if step is None:
                    return range(len(self))

                start = 0
                stop = step * len(self)
            elif step is None:
                step = 1
                start = stop - len(self)
            else:
                start = stop - len(self) * step
        elif stop is None:
            if step is None:
                step = 1
            stop = start + len(self) * step
        elif step is None:
            if self == 0:
                raise TypeError('could not determine range without step')
            delta = stop - start
            if delta > 0:
                delta -= 1
            elif delta < 0:
                delta += 1
            step = int(delta / self)

            if step == 0:
                raise ValueError(
                    'distance too short for {} steps'.format(int(self)))
            if step < self and len(range(start, stop, step)) != len(self):
                raise ValueError(
                    ('step count mismatch ({} != {})'
                     ).format(len(range(start, stop, step)), len(self)))
        else:
            if len(range(start, stop, step)) != len(self):
                raise ValueError(
                    ('step count mismatch ({} != {})'
                     ).format(len(range(start, stop, step)), len(self)))

        return range(start, stop, step)

    def iter_floats(self, start, end):
        # XXX Adjust for float precision quirks?
        factor = (end - start) / self
        for i in range(self):
            yield start + factor * i
        yield end
