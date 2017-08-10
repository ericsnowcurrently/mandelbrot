

def ui(iter_raster, area, grid, scale):
    raise NotImplementedError


def matplotlib(mandelbrot, area):
    import matplotlib.pyplot as plt

    inches = 10
    fig = plt.figure(figsize=(inches, inches), dpi=area.scale.x//inches)

#    for c, i in mandelbrot:
#        # XXX use i
#        plt.plot(c.real, c.imag)

    lines = {}
    for c, i in mandelbrot:
        if i is None:
            # in the set
            continue
        try:
            line = lines[i]
        except KeyError:
            line = lines[i] = []
        line.append((c.real, c.imag))

    for i in sorted(lines):
        print(i, lines[i])
        print()
        #plt.plot([c[0] for c in lines[i]], [c[1] for c in lines[i]])
        #plt.plot(lines[i])
        #plt.fill(lines[i])
        #plt.imshow(lines[i])
        #plt.matshow(lines[i])
        #plt.pcolormesh(lines[i])
        plt.imshow([c[0] for c in lines[i]], [c[1] for c in lines[i]],
                   extent=[area.min.x, area.max.x, area.min.y, area.max.y],
                   interpolation="bicubic")

    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, aspect=1)

    # Shaded rendering
    #light = matplotlib.colors.LightSource(azdeg=315, altdeg=10)
    #M = light.shade(M, cmap=plt.cm.hot, vert_exag=1.5,
    #                norm=colors.PowerNorm(0.3), blend_mode='hsv')

    #plt.imshow(M, extent=[xmin, xmax, ymin, ymax], interpolation="bicubic")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


"""
def mandelbrot_np(radius=1.5, centera=-0.75, centerb=0, scale=100):
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
