from Tkinter import *

class Window(object):

    def __init__(self, width=800, height=600, title='Draw and Learn'):
        self._width = width
        self._height = height
        self.master = Tk()
        self.master.title(title)
        self.master.resizable(False, False)
        self.canvas = Canvas(self.master, width=width, height=height, background='white')
        self.canvas.pack()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def wait(self):
        # TODO run in a separate thread to allow user's program to continue
        self.master.mainloop()

    def line(self, x0, y0, x1, y1, color='black', thickness=1):
        self.canvas.create_line(x0, y0, x1, y1, fill=color, width=thickness)

    def rect(self, x0, y0, x1, y1, color='black', thickness=1, fill=''):
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, fill=fill, width=thickness)

    def circle(self, x, y, radius, color='black', thickness=1, fill=''):
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                outline=color, fill=fill, width=thickness)

    def clear(self):
        self.canvas.delete(ALL)


def rgb(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)
