from pyx import *

class box(canvas.canvas):

    def __init__(self, boundary, boundaryattrs=[deco.stroked], **kwargs):
        canvas.canvas.__init__(self, **kwargs)
        self.boundary = path.normpath(boundary)
        self.draw(self.boundary, boundaryattrs)

    def enlarged(self, enlargeby):
        return box(self.boundary)


c = canvas.canvas()
c.insert(box(path.rect(0, 0, 5, 5)))
c.insert(box(path.rect(0, 0, 5, 5)).enlarged(1))
c.writeEPSfile("newbox")
