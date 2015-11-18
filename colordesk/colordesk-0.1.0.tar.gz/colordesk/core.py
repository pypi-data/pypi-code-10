#!/usr/bin/env python
# coding: utf-8

import yaml
import mistune
from .errors import ParseYAMLError


class ColorDesk(object):
    def __init__(self, title, description=None):
        self.title = title
        self.description = description
        self.description_html = mistune.markdown(description)
        self.palettes = []

    def add_palette(self, p):
        self.palettes.append(p)


def parse_desk_yaml(filedict):

    loop = 0
    for i in yaml.load_all(filedict['text']):
        loop += 1

        if loop == 1:
            if 'meta' in i:
                try:
                    meta = i['meta']
                    title = meta['title']
                    description = meta.get('description')
                except KeyError as e:
                    raise ParseYAMLError('In `meta`: %s' % e)
            else:
                title = filedict['name']
                description = None
            desk = ColorDesk(title, description)
        else:
            palette = dict(i)

            format_palette(palette)

            desk.add_palette(palette)

    return desk


def format_palette(palette):
    """Format & check palette dict"""
    colors = []

    for i in palette['colors']:
        if isinstance(i, basestring):
            color = {
                'name': None,
                'color': i
            }
        else:
            try:
                color = {
                    'name': i['name'],
                    'color': i['color']
                }
            except KeyError as e:
                raise ParseYAMLError('In `colors`: %s' % e)
        colors.append(color)

    palette['colors'] = colors
