
MAX_DEPTH = 100
MAX_ITER = range(MAX_DEPTH)


def iter_mandelbrot(candidates, maxiter=MAX_ITER, _abs=abs):
    """Yield (C, num iterations) for each candidate complex number.

    If C is in the Mandelbrot set then "num iterations" will be None.
    """
    if not hasattr(maxiter, '__iter__'):
        maxiter = range(maxiter) if maxiter else MAX_ITER
    for c in candidates:
        x = 0
        for i in maxiter:
            x = x*x + c
            if _abs(x) > 2:
                yield c, i
                break
        else:
            # in the set!
            yield c, None
