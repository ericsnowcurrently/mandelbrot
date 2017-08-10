
import argparse

from . import imaginary
from ._geometry import Point2D, Area, Grid
from ._mandelbrot import iter_mandelbrot
from .ui import start


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--center',
                        type=(lambda v: Point2D.from_raw(v)),
                        default=(-.75, 0))
    parser.add_argument('--radius', type=float, default=1.5)
    parser.add_argument('--steps', type=int)
    parser.add_argument('--max-iter', dest='scale', type=int)
    parser.add_argument('--numpy', action='store_true')
    parser.add_argument('--ui', dest='uiname', default='text')
    args = parser.parse_args()

    if vars(args).pop('full'):
        args.center = (0, 0)
        args.radius = 2.1

    if args.center and not isinstance(args.center, tuple):
        try:
            a, b = args.center.split(',')
            args.center = (float(a), float(b))
        except (AttributeError, IndexError, ValueError):
            raise
            parser.error('bad center {!r}'.format(args.center))

    if args.scale and args.scale < 0:
        parser.error('got negative --max-iter')

    return args


def main(radius=1.5, center=Point2D(-0.75, 0), steps=None, *,
         numpy=False, scale=None,
         uiname='text'):
    """The program!"""
    if uiname:
        uiname, _, opts = uiname.partition(':')
        uiname = uiname or 'text'
        opts = opts.split(';')
    else:
        uiname = 'text'
        opts = None
    if not steps:
        if not uiname or uiname.startswith('text'):
            steps = 40
        else:
            steps = 400
    grid = Grid(steps, steps)
    area = Area.from_radius(radius, center)
    #scale = Scale.from_raw(scale)

    if numpy:
        raise NotImplementedError
    else:
        def iter_raster(area, grid, scale):
            candidates = imaginary.iter_raster(area, grid)
            return iter_mandelbrot(candidates, scale)

    ui = start(uiname, opts, area, grid, scale, iter_raster)
    if ui is not None:
        ui.wait()


if __name__ == '__main__':
    args = parse_args()
    main(**vars(args))


"""
def mandelbrot_np(radius=1.5, centera=-0.75, centerb=0, scale=400):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt

    xmin, xmax, xn = centera - radius, centera + radius, scale + 1
    ymin, ymax, yn = centerb - radius, centerb + radius, scale + 1
    X = np.linspace(xmin, xmax, xn, dtype=np.float32)
    Y = np.linspace(ymin, ymax, yn, dtype=np.float32)
    C = X + Y[:, None]*1j
    N = np.zeros(C.shape, dtype=int)

    candidates = _iter_c5(radius, centera, centerb, scale)
    for c, i in _mandelbrot5(candidates, MAX_ITER):
        N[c] = i

    dpi = 72
    width = 10
    height = 10*yn/xn
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, aspect=1)
    # Shaded rendering
    #light = matplotlib.colors.LightSource(azdeg=315, altdeg=10)
    #M = light.shade(M, cmap=plt.cm.hot, vert_exag=1.5,
    #                norm=colors.PowerNorm(0.3), blend_mode='hsv')
    plt.imshow(M, extent=[xmin, xmax, ymin, ymax], interpolation="bicubic")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
"""
