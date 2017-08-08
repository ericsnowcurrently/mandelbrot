
import math


MAX_DEPTH = 100
MAX_ITER = range(MAX_DEPTH)


def mandelbrot1(mina, maxa, minb, maxb, scale):
    da = maxa - mina
    scalea = scale
    factora = da / scalea
    stepsa = range(scalea + 1)

    db = maxb - minb
    #scaleb = int(scalea * min(db/da, da/db))
    scaleb = int(scalea * db/da)
    factorb = db / scaleb  # XXX floats not ideal?
    stepsb = range(scaleb + 1)

    #plot = [[None] * (scalea + 1)
    #        for _ in range(scaleb + 1)]
    for stepb in stepsb:
        b = factorb * stepb + minb
        #print(minb, ' ', end='')
        for stepa in stepsa:
            a = factora * stepa + mina
            c = a + b * 1j

            x = 0
            for i in MAX_ITER:
                x = x*x + c
                if abs(x) > 4:
                    print('X', end='')
                    #plot[b][a] = i
                    break
            else:
                # in the set!
                print(' ', end='')
                #plot[b][a] = None
        print()
        #print(' {:.01f}'.format(b))

    last = math.floor(mina)
    if math.floor(factora + mina) > last:
        last -= 1
    print(mina, end='')
    used = len(str(mina))
    for stepa in range(1, scalea):
        a = factora * stepa + mina
        if math.floor(a) > last:
            last = math.floor(a)
            used = len(str(last))
            print(last, end='')
        elif used:
            used -= 1
        else:
            print(' ', end='')
    print() if used else print(maxa)


def mandelbrot2(radius=1.5, centera=-0.75, centerb=0, scale=100):
    factor = radius * 2 / scale  # XXX floats not ideal?

    mina = centera - radius
    stepsa = range(int(scale) + 1)

    minb = centerb - radius
    stepsb = range(int(scale), -1, -1)

    for stepb in stepsb:
        b = factor * stepb + minb
        for stepa in stepsa:
            a = factor * stepa + mina
            c = a + b * 1j

            x = 0
            for i in MAX_ITER:
                x = x*x + c
                if abs(x) > 2:
                    if i == 0:
                        print('..', end='')
                    elif i == 1:
                        print('\'\'', end='')
                    elif i == 2:
                        print('""', end='')
                    elif i == 3:
                        print('++', end='')
                    elif i == 4:
                        print('**', end='')
                    elif 5 <= i < 20:
                        print('XX', end='')
                    else:
                        print('##', end='')
                    break
            else:
                # in the set!
                print('  ', end='')
        print()


def _mandelbrot3(mina, minb, stepsa, stepsb, factora, factorb):
    baserow = [None] * (len(stepsa) + 1)
    for stepb in stepsb:
        b = factorb * stepb + minb
        row = list(baserow)
        gi = 0
        for stepa in stepsa:
            a = factora * stepa + mina
            c = a + b * 1j

            x = 0
            for i in MAX_ITER:
                x = x*x + c
                if abs(x) > 2:
                    row[gi] = i
                    break
            else:
                # in the set!
                pass  # row[gi] = None
            gi += 1
        yield row


def mandelbrot3(radius=1.5, centera=-0.75, centerb=0, scale=100):
    factor = radius * 2 / scale  # XXX floats not ideal?
    mina = centera - radius
    stepsa = range(int(scale) + 1)
    minb = centerb - radius
    stepsb = range(int(scale), -1, -1)
    for row in _mandelbrot3(mina, minb, stepsa, stepsb, factor, factor):
        for i in row:
            if i is None:
                print('  ', end='')
            elif i == 0:
                print('..', end='')
            elif i == 1:
                print('\'\'', end='')
            elif i == 2:
                print('""', end='')
            elif i == 3:
                print('++', end='')
            elif i == 4:
                print('**', end='')
            elif 5 <= i < 20:
                print('XX', end='')
            else:
                print('##', end='')
        print()


if __name__ == '__main__':
    #mandelbrot1(-4, 1, -2.5, 2.5, 40)
    #mandelbrot1(-1.5, 0, -0.5, 0.5, 100)
    #mandelbrot1(-2.1, 2.1, -2.1, 2.1, 400)

    #mandelbrot2(scale=500)
    #mandelbrot2(2.1, 0, 0, 400)

    #mandelbrot3(scale=500)
    mandelbrot3(2.1, 0, 0, 400)
