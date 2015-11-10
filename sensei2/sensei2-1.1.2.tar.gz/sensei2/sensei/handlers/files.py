from cStringIO import StringIO
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image
from random import randint, choice
from sensei2.sensei.handlers.base import BaseHandler


class ImageFieldHandler(BaseHandler):
    def __init__(self):
        super(ImageFieldHandler, self).__init__()
        self.handled_class = models.ImageField

    def object_mode(self, obj, field, sensei):
        width = randint(100, 200)
        height = randint(100, 200)

        image = Image.new("RGBA", (width, height), (
            choice((randint(0, 51), randint(102, 153), randint(204, 255))),
            choice((randint(0, 51), randint(102, 153), randint(204, 255))),
            choice((randint(0, 51), randint(102, 153), randint(204, 255))),
        ))
        i = StringIO()
        image.save(i, format="png")
        getattr(obj, field.attname).save("sensei_image.png", ContentFile(i.getvalue()), save=False)


class FileFieldHandler(ImageFieldHandler):
    def __init__(self):
        super(FileFieldHandler, self).__init__()
        self.handled_class = models.FileField
