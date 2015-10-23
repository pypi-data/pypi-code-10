import os
import re
from . import utils


SASS_IMPORT_RE = re.compile(r"""@import\s+['"](.+?\.s[ca]ss)['"]\s*;""")


def _read_sass_imports(file):
    deps = []
    with open(file) as f:
        sassfile = f.read()
    imports = SASS_IMPORT_RE.findall(sassfile)
    sass_dir = os.path.dirname(file)

    for imp in imports:
        if os.path.isabs(imp):
            deps.append(imp)
        elif os.path.isfile(os.path.join(sass_dir, imp)):
            deps.append(os.path.abspath(os.path.join(sass_dir, imp)))
        else:
            raise ValueError('Invalid LESS import in {}: {}'.format(file, imp))
    return deps


def sass_dependencies(input_file):
    return utils.breadth_first_search(_read_sass_imports, input_file)


def sass_compile(input_file, output_file, release=False):
    map_file = output_file + '.map'
    output_style = 'compressed' if release else 'expanded'
    source_map = '--source-comments --source-map-embed --source-map-contents --source-map {}'.format(map_file) if not release else ''

    cmdline = [
        utils.get_node_bin_dir('node-sass'),
        '--output-style',
        output_style,
        source_map,
        input_file,
        output_file,
    ]

    try:
        utils.ensure_deleted(map_file)
        utils.run_command(cmdline, 'Failed to compile SASS to "{}"'.format(output_file))
    except:
        utils.ensure_deleted(output_file)
        raise
    finally:
        utils.ensure_deleted(map_file)
