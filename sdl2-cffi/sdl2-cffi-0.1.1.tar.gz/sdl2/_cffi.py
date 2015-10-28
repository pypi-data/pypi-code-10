from cffi import FFI
from subprocess import check_output
import re
import os
import pycparser
import json
import itertools
from pycparser import c_ast
from pycparser.c_generator import CGenerator

INCLUDE_PATTERN = re.compile(r'(-I)?(.*SDL2)')
DEFINE_PATTERN = re.compile(r'^#define\s+(\w+)\s+\(?([\w<|.]+)\)?', re.M)
DEFINE_BLACKLIST = [
    'SDL_ANDROID_EXTERNAL_STORAGE_READ',
    'SDL_ANDROID_EXTERNAL_STORAGE_WRITE',
    'M_PI',
    'main',
    'SDL_main',
    'SDL_AUDIOCVT_PACKED'
]
FUNCTION_BLACKLIST = [
    'SDL_main'
]
VARIADIC_ARG_PATTERN = re.compile(r'va_list \w+')
ARRAY_SIZEOF_PATTERN = re.compile(r'\[[^\]]*sizeof[^\]]*]')

HEADERS = [
    'SDL_main.h',
    'SDL_stdinc.h',
    'SDL_atomic.h',
    'SDL_audio.h',
    'SDL_clipboard.h',
    'SDL_cpuinfo.h',
    'SDL_endian.h',
    'SDL_error.h',
    'SDL_scancode.h',
    'SDL_keycode.h',
    'SDL_keyboard.h',
    'SDL_joystick.h',
    'SDL_touch.h',
    'SDL_gesture.h',
    'SDL_events.h',
    'SDL_filesystem.h',
    'SDL_gamecontroller.h',
    'SDL_haptic.h',
    'SDL_hints.h',
    'SDL_loadso.h',
    'SDL_log.h',
    'SDL_messagebox.h',
    'SDL_mutex.h',
    'SDL_power.h',
    'SDL_render.h',
    'SDL_rwops.h',
    'SDL_system.h',
    'SDL_thread.h',
    'SDL_timer.h',
    'SDL_version.h',
    'SDL_video.h',
    'SDL.h'
]

ffi = FFI()
cflags = check_output(['sdl2-config', '--cflags']).decode('utf-8').strip()
cflags_libs = check_output(['sdl2-config', '--libs']).decode('utf-8').strip()

include_dir = INCLUDE_PATTERN.search(cflags).group(2)

ffi.set_source(
    '_sdl2',
    '#include "SDL.h"',
    extra_compile_args=cflags.split(),
    extra_link_args=cflags_libs.split()
)

# define GCC specific compiler extensions away
DEFINE_ARGS = [
    '-D__attribute__(x)=',
    '-D__inline=',
    '-D__restrict=',
    '-D__extension__=',
    '-D__GNUC_VA_LIST=',
    '-D__gnuc_va_list=void*',
    '-D__asm__(x)=',
    '-D__inline__=',
    '-DDOXYGEN_SHOULD_IGNORE_THIS='
]

ast = pycparser.parse_file(os.sep.join([include_dir, 'SDL.h']),
                           use_cpp=True, cpp_args=DEFINE_ARGS)


class Collector(c_ast.NodeVisitor):
    TYPEDEF_BLACKLIST = re.compile(r'fd_set')

    def __init__(self):
        self.generator = CGenerator()
        self.typedecls = []
        self.functions = []

    def process_typedecl(self, node):
        if node.coord is None or node.coord.file.find(include_dir) != -1:
            typedecl = '{};'.format(self.generator.visit(node))
            typedecl = ARRAY_SIZEOF_PATTERN.sub('[...]', typedecl)
            self.typedecls.append(typedecl)

    def sanitize_enum(self, enum):
        for name, enumeratorlist in enum.children():
            for name, enumerator in enumeratorlist.children():
                enumerator.value = c_ast.Constant('dummy', '...')
        return enum

    def visit_Typedef(self, node):
        if node.coord is None or node.coord.file.find(include_dir) != -1:
            if ((isinstance(node.type, c_ast.TypeDecl) and
                 isinstance(node.type.type, c_ast.Enum))):
                self.sanitize_enum(node.type.type)
            self.process_typedecl(node)

    def visit_Union(self, node):
        self.process_typedecl(node)

    def visit_Struct(self, node):
        self.process_typedecl(node)

    def visit_Enum(self, node):
        if node.coord is None or node.coord.file.find(include_dir) != -1:
            node = self.sanitize_enum(node)
            self.process_typedecl(node)

    def visit_FuncDecl(self, node):
        if node.coord is None or node.coord.file.find(include_dir) != -1:
            if isinstance(node.type, c_ast.PtrDecl):
                function_name = node.type.type.declname
            else:
                function_name = node.type.declname
            if function_name in FUNCTION_BLACKLIST:
                return
            decl = '{};'.format(self.generator.visit(node))
            decl = VARIADIC_ARG_PATTERN.sub('...', decl)
            self.functions.append(decl)

collector = Collector()
collector.visit(ast)

defines = set()
for header_path in HEADERS:
    with open(os.sep.join([include_dir, header_path]), 'r') as header_file:
        header = header_file.read()
        for match in DEFINE_PATTERN.finditer(header):
            if match.group(1) in DEFINE_BLACKLIST:
                continue
            try:
                int(match.group(2), 0)
                defines.add('#define {} {}'.format(match.group(1),
                                                   match.group(2)))
            except:
                defines.add('#define {} ...'.format(match.group(1)))

print('Processing {} defines, {} types, {} functions'.format(
    len(defines),
    len(collector.typedecls),
    len(collector.functions)
))
ffi.cdef('\n'.join(itertools.chain(*[
    defines,
    collector.typedecls,
    collector.functions
])))
