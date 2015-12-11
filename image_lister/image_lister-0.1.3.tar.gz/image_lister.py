import sys
import os
from collections import Counter


def get_listing(path):
    return os.listdir(path)


def get_execute_path(args):
    return args[0]


def extension(filename):
    return filename.split('.')[-1]


def is_image(fname):
    image_extensions = ['jpg', 'png', 'tiff']
    if extension(fname) in image_extensions:
        return True
    return False


def main(args=None):
    if not args:
        args = sys.argv

    if len(args) > 1:
        for i, arg in enumerate(args):
            print("%d = %s" % (i, arg))
        list_path = args[1]
    else:
        list_path = get_execute_path(args)

    files = get_listing(list_path)
    images = [fname for fname in files if is_image(fname)]
    jpeg_count = sum(
        [1 for iname in images if extension(iname) in ['jpg', 'jpeg']])
    png_count = sum([1 for iname in images if extension(iname) == 'png'])
    for image in images:
        print(image)

    # Obviously this is very crude. It will count files
    # that are not images but have image extensions too.
    # Would later incorporate use of https://github.com/ahupp/python-magic
    extension_list = [extension(iname) for iname in images]
    type_counts = Counter(extension_list)

    jpeg_count = type_counts['jpeg'] + type_counts['jpg']
    png_count = type_counts['png']
    tiff_count = type_counts['tiff']

    print("\nTotal JPEG count: %d" % jpeg_count)
    print("\nTotal PNG count: %d" % png_count)
    print("\nTotal TIFF count: %d" % tiff_count)
    print("\nTotal images found in this directory: %d\n" % len(images))

if __name__ == '__main__':
    main(sys.argv)
