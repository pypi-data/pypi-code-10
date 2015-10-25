import json
import os
from os import path
from .provider import Provider

SOURCE_DIR = "../source/data/"


class AWS(Provider):

    def __init__(self, options, *args, **kwargs):
        data_file = path.join(os.path.dirname(os.path.abspath(__file__)), SOURCE_DIR, 'aws.json')
        super(AWS, self).__init__(data_file, options, *args, **kwargs)

    @property
    def ec2_region(self):
        return self.data['ec2']['region']

    @property
    def ec2_zone(self):
        return self.data['ec2']['zone']

    @property
    def ec2_instance_type(self):
        return self.data['ec2']['instance-type']

    def render_ec2_region(self):
        return self.render(self.ec2_region)

    def render_ec2_zone(self):
        return self.render(self.ec2_zone)

    def render_ec2_instance_type(self):
        return self.render(self.ec2_instance_type)
