

def ui(iter_raster, area, grid, scale, *, static=False):
    values = iter_raster(area, grid, scale)
    if static:
        tk(values, grid)
    else:
        raise NotImplementedError


def _ppm(values, grid):
    image = b'P6 %d %d 255 ' % (len(grid.width), len(grid.height))
    for _, i in values:
        if i is None:
            image += b'\x00\x00\x00'
        elif i < 5:
            image += bytes([max(1, 255 - i * 20), 0, 0])
        elif i < 20:
            image += bytes([0, max(1, 255 - i * 20), 0])
        else:
            #image += bytes([max(1, 255 - i * 4)] * 3)
            image += bytes([0, 0, max(1, 255 - i * 4)])
    return image


def tk(values, grid):
    import tkinter as tk

    root = tk.Tk()
    canvas = tk.Canvas(root, width=len(grid.width), height=len(grid.height))
    canvas.pack()

    data = _ppm(values, grid)
    bitmap = tk.PhotoImage(data=data, format='PPM')
    canvas.create_image(0, 0,
                        image=bitmap,
                        anchor=tk.NW)

    tk.mainloop()
