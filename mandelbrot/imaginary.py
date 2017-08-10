

def iter_raster(area, grid):
    coords = grid.iter_floats(area.min.x, area.max.x, area.max.y, area.min.y)
    for a, b in coords:
        yield a + b * 1j


#def iter_area(min=MIN, max=MAX, scalea=SCALE, scaleb=None):
#    """Yield each number on the imaginary plane.
#
#    Given that the plane is continuous, only a discrete number of points
#    in a finite area of the plane.  The area is bounded by the points
#    (or complex numbers) "min" and "max".  "scalea" and "scaleb" dictate
#    the selection of points within the area.  The domain and range are
#    divided into equal intervals and the points at the corners or the
#    intervals are the results.
#
#    The order of the points is top-down, left-to-right.  This means
#    each cartesian row is yielded in order, followed by each successive
#    row.
#
#    By default, "scaleb" is "scalea" proportioned according to dy/dx.
#    The other defaults result in a high-level view of the plane framed
#    just around the Mandelbrot set.
#    """
#    if not min and not max:
#        min, max = MIN, MAX
#    else:
#        mina, minb = Point.from_raw(min)
#        maxa, maxb = Point.from_raw(max)
#        if mina >= maxa or minb >= maxb:
#            raise ValueError('min must be below and left of max')
#    scalea = int(scalea) if scalea else SCALE
#    scaleb = int(scaleb) if scaleb else None
#
#    da = maxa - mina
#    factora = da / scalea
#    stepsa = range(scalea + 1)  # left-to-right
#
#    db = maxb - minb
#    scaleb if scaleb else int(scalea * db/da)
#    factorb = db / scaleb
#    stepsb = range(scaleb, -1, -1)  # top-down
#
#    for stepb in stepsb:
#        b = factorb * stepb + minb
#        for stepa in stepsa:
#            a = factora * stepa + mina
#            yield a + b * 1j  # c
