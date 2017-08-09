
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
