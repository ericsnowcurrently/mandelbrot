

def start(kind, opts, area, grid, scale, iter_raster):
    kwargs = {}
    if kind == 'text':
        if 'flat' in opts:
            kwargs['spec'] = {'*': 'XX'}
        from ._text import render as start
    else:
        raise ValueError('unsupported UI {!r}'.format(kind))
    return start(iter_raster, area, grid, scale, **kwargs)
