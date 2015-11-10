import want
import sys
import getopt


def main(argv):
    if len(argv) == 0:
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, 'has:r:', ['help', 'all', 'size='])
    except getopt.GetoptError as err:
        usage()
        sys.exit(str(err))
    if not opts:
        want.get_photo(args[0], 10000, 200000)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-s', '--size'):
            size = a.split('-')
            min_size = int(size[0])
            max_size = int(size[1])
            want.get_photo(args[0], min_size, max_size)
        elif o in ('-a', '--all'):
            want.get_photo(args[0], -1, 100000000)
        elif o in ('-r'):
            want.get_all(a, want.get_photo)


def usage():
    print('usage: want [options] [--]')
    print('')
    print('    -h, --help            help')
    print('    -a <url>              download all image from url')
    print('    -s, --size 100-10000  download 100bytes~10000bytes image')
    print('    -r <urls.txt>         download from urls.txt')
    print('')
    print('    NOTE: if no -s flag it will default 10000-200000')


if __name__ == '__main__':
    main(sys.argv[1:])
