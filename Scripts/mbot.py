

def get_nums(xmin, xmax, ymin, ymax, scale):
    xscale = int(scale)
    xfactor = (xmax - xmin) / xscale
    xsteps = range(xscale + 1)

    yscale = int(scale * (ymax - ymin)/(xmax - xmin))
    yfactor = (ymax - ymin) / yscale
    ysteps = range(yscale, -1, -1)

    for y in ysteps:
        b = y * yfactor + ymin
        for x in xsteps:
            a = x * xfactor + xmin
            yield a + b * 1j


def mandelbrot(xmin, xmax, ymin, ymax, scale, maxiter):
    for c in get_nums(xmin, xmax, ymin, ymax, scale):
        z = 0j
        for i in range(maxiter):
            z = z*z + c
            if z.real**2 + z.imag**2 > 4:
                # not mandelbrot
                yield c, i
                break
        else:
            # is mandelbrot
            yield c, None


def main(*args):
    args = [float(a) for a in args]
    xmin, xmax, ymin, ymax, scale = args

    step = 0
    for c, i in mandelbrot(*args, maxiter=100):
        if i is None:
            print('  ', end='')
        else:
            print('XX', end='')
        if step == scale:
            print()
            step = 0
        else:
            step += 1


import sys
main(*sys.argv[1:])
