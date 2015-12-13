import os
import sys
import shutil
import argparse

import yaml
import jinja2
import markdown


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config',
        help="config file to load", default='config.yaml')

    parser.add_argument('-D', '--dry',
        help="don't write any files", action='store_true')

    parser.add_argument('-d', '--debug',
        help="enable debug mode", action='store_true')

    parser.add_argument('-s', '--serve',
        help="serve the project after building", action='store_true')

    return parser.parse_args()

args = get_args()


def get_config(config_file_path):
    try:
        config_file = open(config_file_path)
        config = yaml.load(config_file)
        config_file.close()
    except IOError as e:
        print("Couldn't load config file: {0}".format(e))
        raise SystemExit

    defaults = {
        'content_dir': 'content',
        'content_static_dir': 'content/static',
        'layout_dir': 'layout',
        'layout_static_dir': 'layout/static',
        'build_dir': 'build',
        'build_static_dir': 'build/static'
    }

    for key, val in defaults.items():
        if key not in config:
            config[key] = value

    return config

config = get_config(args.config)


class ContentDir(object):
    def __init__(self, content_list, parent=None):
        main_path = os.getcwd() + '/' + config['content_dir']

        self.contents = []
        self.parent = parent

        if type(content_list) == list:
            self.path = main_path
            self.base_name = config['content_dir']

            for item in content_list:
                if type(item) == dict:
                    self.contents.append(ContentDir(item, parent=self))
                else:
                    self.contents.append(ContentItem(item, parent=self))

        elif type(content_list) == dict:
            for item, contents in content_list.items():
                self.path = parent.path + '/' + item
                self.base_name = item

                for item in contents:
                    if type(item) == dict:
                        self.contents.append(ContentDir(item, parent=self))
                    else:
                        self.contents.append(ContentItem(item, parent=self))

        else: raise ValueError('invalid type for content_list argument')

    def walk(self):
        for item in self:
            if type(item) == ContentDir:
                for item2 in item.walk():
                    yield item2
            else:
                yield item

    def __unicode__(self):
        return self.base_name
    __str__ = __unicode__

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            result = self.contents[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result
    next = __next__


class ContentItem(object):
    def __init__(self, file_name, parent):
        if ':' in file_name:
            self.file_name = file_name.split(':')[0]
            self.template = file_name.split(':')[1]
        else:
            self.file_name = file_name
            self.template = config['main_template']

        self.path = parent.path + '/' + self.file_name

        if type(parent) == ContentDir or parent == None: self.parent = parent
        else: raise ValueError('parent argument must be a ContentDir or None')

    def get_link(self):
        pass

    def get_prev(self):
        pass

    def get_next(self):
        pass

    def __unicode__(self):
        return self.file_name
    __str__ = __unicode__


def db_print(string, level):
    if level == 1 and args.debug:
        print(string)
    elif level == 0:
        print(string)


def copy_static():
    for dir_path, dirs, file_names in os.walk(config['layout_static_dir']):
        for file_name in file_names:
            old_path = dir_path + '/' + file_name
            new_path = old_path.replace(config['layout_static_dir'],
                                        config['build_static_dir'])
            try:
                shutil.copyfile(old_path, new_path)
            except IOError:
                os.makedirs(os.path.dirname(new_path))
                shutil.copyfile(old_path, new_path)

    for dir_path, dirs, file_names in os.walk(config['content_static_dir']):
        for file_name in file_names:
            old_path = dir_path + '/' + file_name
            new_path = old_path.replace(config['content_static_dir'],
                                        config['build_static_dir'])
            try:
                shutil.copyfile(old_path, new_path)
            except IOError:
                os.makedirs(os.path.dirname(new_path))
                shutil.copyfile(old_path, new_path)


def main():
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    jinja = jinja2.Environment(
        loader=jinja2.FileSystemLoader(config['layout_dir']),
        trim_blocks=True
    )

    content = ContentDir(config['content'])
    for item in content.walk():
        new_path = item.path.replace(config['content_dir'], config['build_dir'])
        new_path = new_path.rpartition('.')[0] + '.html'

        input_file = open(item.path)
        md_html = md.convert(input_file.read())

        for key, val in md.Meta.items():
            if len(val) == 1:
                md.Meta[key] = val[0]

        context = {'content': md_html, 'content_list': config['content']}
        context.update(md.Meta)
        end_html = jinja.get_template(item.template).render(**context)

        try:
            output_file = open(new_path, 'w+')
        except IOError:
            os.makedirs(os.path.dirname(new_path))
            output_file = open(new_path, 'w+')

        output_file.write(end_html)

        md.reset()
        input_file.close()
        output_file.close()




    copy_static()


def serve():
    try:
        import http.server as httpserver
        import socketserver
    except ImportError:
        import SimpleHTTPServer as httpserver
        import SocketServer as socketserver

    try:
        os.chdir(config['build_dir'])
    except:
        os.makedirs(config['build_dir'])
        os.chdir(config['build_dir'])

    Handler = httpserver.SimpleHTTPRequestHandler

    print("Serving at port 8000!")
    socketserver.TCPServer(("", 8000), Handler).serve_forever()


if __name__ == '__main__':
    main()
    if args.serve:
        serve()
