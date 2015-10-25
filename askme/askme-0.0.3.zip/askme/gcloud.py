import json
import os
from os import path
from .provider import Provider

SOURCE_DIR = "../source/data/"


class GCloud(Provider):

    def __init__(self, options, *args, **kwargs):
        data_file = path.join(os.path.dirname(os.path.abspath(__file__)), SOURCE_DIR, 'gcloud.json')
        super(GCloud, self).__init__(data_file, options, *args, **kwargs)

    @property
    def gce_zone(self):
        return self.data['gce']['zone']

    @property
    def gce_machine_type(self):
        return self.data['gce']['machine-type']

    @property
    def gce_disk_type(self):
        return self.data['gce']['disk-type']

    @property
    def gce_image(self):
        return self.data['gce']['image']

    def render_gce_zone(self):
        return self.render(self.gce_zone)

    def render_gce_machine_type(self):
        return self.render(self.gce_machine_type)

    def render_gce_disk_type(self):
        return self.render(self.gce_disk_type)

    def render_gce_image(self):
        return self.render(self.gce_image)
