
from mandelbrot._geometry import Area


def ui(iter_raster, area, grid, scale, *, static=False):
    values = iter_raster(area, grid, scale)
    if static:
        tk(values, grid)
    else:
        tk_dynamic(values, grid, iter_raster, area, scale)


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


def tk_dynamic(values, grid, iter_raster, area, scale):
    import tkinter as tk

    root = tk.Tk()
    frame = tk.Frame(root, width=len(grid.width), height=len(grid.height))
    frame.pack()

    def zoom(event):
        # event.delta ...
        if event.num == 4:  # scroll up
            factor = 2
        else:  # scroll down
            factor = 0.5
        xmin = event.x - factor * grid.width / 2
        xmax = event.x + factor * grid.width / 2
        ymin = event.y - factor * grid.height / 2
        ymax = event.y + factor * grid.height / 2
        newarea = Area((xmin, ymin), (xmax, ymax))
        values = iter_raster(newarea, grid, scale)

        data = _ppm(values, grid)
        bitmap = tk.PhotoImage(data=data, format='PPM')
        canvas.itemconfig(image, image=bitmap)

    canvas = tk.Canvas(frame, width=len(grid.width), height=len(grid.height))
    #canvas.bind("<MouseWheel>", zoom)
    canvas.bind("<Button-4>", zoom)
    canvas.bind("<Button-5>", zoom)
    canvas.pack()

    data = _ppm(values, grid)
    bitmap = tk.PhotoImage(data=data, format='PPM')
    image = canvas.create_image(0, 0,
                                image=bitmap,
                                anchor=tk.NW)

    tk.mainloop()
