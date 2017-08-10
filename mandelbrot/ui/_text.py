
from mandelbrot._util import as_namedtuple


SCALE_TEXT = 40
CHARS = {
        None: '  ',
        0: '..',
        1: "''",
        2: '""',
        3: '++',
        4: '**',
        '5-19': 'XX',
        '*': '##',
        }


@as_namedtuple('chars matched default')
class Spec:

    @classmethod
    def from_raw(cls, raw):
        if raw is None:
            raw = CHARS
        elif isinstance(raw, Spec):
            return raw

        return cls.from_chars(raw)

    @classmethod
    def from_chars(cls, chars=CHARS):
        if not chars:
            chars = CHARS
        elif not hasattr(chars, 'items'):
            chars = enumerate(chars)
        chars = dict(chars)

        matched = '  '
        default = '##'
        for i in list(chars):
            if isinstance(i, int):
                if i < 0:
                    raise ValueError(
                            'expected non-negative index, got {}'.format(i))
                continue
            if i is None:
                matched = chars.pop(i)
            elif i == '*':
                default = chars.pop(i)
            elif isinstance(i, str):
                char = chars.pop(i)
                mini, maxi = i.split('-')
                mini, maxi = int(mini), int(maxi)
                if mini >= maxi:
                    raise ValueError('non-increasing index {!r}'.format(i))
                for subi in range(mini, maxi + 1):
                    if subi in chars:
                        raise ValueError('duplicate index in {!r}'.format(i))
                    chars[subi] = char
            else:
                raise ValueError('bad index {!r}'.format(i))

        for i in range(len(chars)):
            if i not in chars:
                raise ValueError('missing chars index {}'.format(i))

        return cls(chars, matched, default)


def render(iter_raster, area, grid, scale, spec=None):
    steps = int(grid.width) if grid else SCALE_TEXT
    if steps <= 0:
        raise ValueError('got non-positive steps')
    spec = Spec.from_raw(spec)
    _text(iter_raster, area, grid, scale, spec)


def _text(iter_raster, area, grid, scale, spec):
    chars, matched, default = spec
    values = iter_raster(area, grid, scale)
    step = 0
    for _, i in values:
        if i is None:
            print(matched, end='')
        else:
            print(chars.get(i, default), end='')

        if step == grid.width:
            print()
            step = 0
        else:
            step += 1
