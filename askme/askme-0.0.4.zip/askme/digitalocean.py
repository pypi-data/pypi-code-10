import json
import os
from os import path
from .provider import Provider

SOURCE_DIR = "./source/data/"


class DigitalOcean(Provider):

    def __init__(self, options, *args, **kwargs):
        data_file = path.join(os.path.dirname(os.path.abspath(__file__)), SOURCE_DIR, 'digitalocean.json')
        super(DigitalOcean, self).__init__(data_file, options, *args, **kwargs)

    @property
    def region(self):
        return self.data['region']

    @property
    def size(self):
        return self.data['size']

    @property
    def dist_image(self):
        return self.data['image']['dist']

    @property
    def app_image(self):
        return self.data['image']['app']

    def render_region(self):
        return self.render(self.region)

    def render_size(self):
        return self.render(self.size)

    def render_dist_image(self):
        return self.render(self.dist_image)

    def render_app_image(self):
        return self.render(self.app_image)
