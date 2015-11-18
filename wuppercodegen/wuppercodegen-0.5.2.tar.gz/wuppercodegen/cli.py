#!/usr/bin/env python
#
# Copyright 2014-2015 Mark Donszelmann, Jose Valenciano and Jorn Schumacher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# WupperCodeGen
#
# Code generator based on a Register Map (YAML) and templates (Jinja2).
#
# Authors: Mark Donszelmann (Mark.Donszelmann@cern.ch), Jose Valenciano, Jorn Schumacher (Jorn Schumacher@cern.ch)
#

import jinja2
import yaml
import copy
import argparse
import re
import types
import inspect
import sys

from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, exists, getmtime
from operator import itemgetter, attrgetter, methodcaller

from version import __version__

class FileLoader(BaseLoader):
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with file(path) as f:
            source = f.read().decode('utf-8')
        return source, path, lambda: mtime == getmtime(path)

class Node(object):
    not_inherited = [ 'parent', 'nodes', 'name', 'full_name',
                      'dot_name', 'prefix_name',
                      'offset', 'address', 'entries', 'ref',
                      'index', 'number',
                      'is_bitfield', 'is_register', 'is_group' ]

    def __init__(self, parent, dictionary, name):
        self.parent = parent
        self.nodes = []
        self.offset = 0
        self.address = 0
        self.entries = []
        self.is_bitfield = False
        self.is_register = False
        self.is_group = False
        self.is_sequence = False
        # FIXME move up when entries is dealt with
        for k, v in dictionary.items():
            setattr(self, k, v)
        self.name = name

    def __getattr__(self, attr):
#        print self.name, "__getattr__ ", attr
        if attr in Node.not_inherited:
            raise AttributeError("Attribute '"+attr+"'' not defined in node '"+self.name+"'")
        if self.parent != None:
            return getattr(self.parent, attr)
        else:
            return None

    def __getattribute__(self, attr):
        # lookup value as usual but allow for function calls without arguments to be called as attributes
        val = super(Node, self).__getattribute__(attr)

        if callable(val):
            argcount = len(inspect.getargspec(val).args)
            # Account for self
            if argcount == 1:
                return val()
            else:
                return val
        else:
            return val

    def is_write(self):
        return self.type == 'W'

    def is_trigger(self):
        return self.type == 'T'

    def is_read(self):
        return self.type == 'R'

    def has_write_bitfields(self):
        if self.is_register:
            for bf in self.bitfield:
                if bf.type == 'W': return True
        return False

    def has_trigger_bitfields(self):
        if self.is_register:
            for bf in self.bitfield:
                if bf.type == 'T': return True
        return False

    def has_read_bitfields(self):
        if self.is_register:
            for bf in self.bitfield:
                if bf.type == 'R': return True
        return False

    def full_name(self):
        return self.name

class BitField(Node):
    def __init__(self, parent, dictionary, name):
        Node.__init__(self, parent, dictionary, name)
        self.is_bitfield = True
        if self.name == None: self.name = ''

    def bits(self):
        return self.hi - self.lo + 1

    def full_name(self):
        return self.parent.full_name.format(bitfield='_'+self.name)

    def dot_name(self):
        return self.parent.full_name.format(bitfield='.'+self.name)

class Register(Node):
    def __init__(self, parent, dictionary, name):
        Node.__init__(self, parent, dictionary, name)
        self.is_register = True
        self.index = None

    def lo(self):
        lo = sys.maxint
        for bf in self.bitfield:
            lo = min(lo,bf.lo)
        return lo

    def hi(self):
        hi = -sys.maxint-1
        for bf in self.bitfield:
            hi = max(hi,bf.hi)
        return hi

    def bits(self):
        return self.hi - self.lo + 1

    def full_name(self):
        return self.name if self.index == None else self.name.format(index=self.index,bitfield='{bitfield}')

    def prefix_name(self):
        return self.full_name.replace('{bitfield}','')

    def sort_by_address(self):
        return 0.0

class Group(Node):
    def __init__(self, parent, dictionary, name):
        Node.__init__(self, parent, dictionary, name)
        self.is_group = True

class Sequence(Group):
    def __init__(self, parent, dictionary, name, number, index):
        Group.__init__(self, parent, dictionary, name)
        self.is_sequence = True
        self.number = number
        self.index = index

    def full_name(self):
        return self.name if '{' not in self.name else self.name.format(index=self.index)

def read_input(yaml_file):
    """Read data from input yaml file"""

    with open(yaml_file, 'r') as f:
        config=yaml.load(f)

    return config

def generate_bitfields(register):
    """Define the bitfields"""
    bitfields = []
    bitfieldByName = {}

    # set inherited keys in bitfields
    bfs = register.bitfield
    for bfDict in bfs:
        name = bfDict['name'] if 'name' in bfDict else None
        bf = BitField(register, bfDict, name)

        # set parameters and extra parameters
        if isinstance(bf.range, str):
            if bf.range == 'any':
                bf.hi,bf.lo = -1,0;
            else:
                x = bf.range.split("..")
                bf.hi = int(x[0])
                bf.lo = int(x[1])
        else:
            bf.hi,bf.lo = bf.range,bf.range

        bitfields.append(bf)
        bitfieldByName[bf.name] = bf

    register.bitfield = bitfields
    register.bitfieldByName = bitfieldByName

    return bitfields

def generate_register(parent, register, registers, nodes, address, index):
    """Define a register"""

    if 'name' not in register:
        print "ERROR no 'name' defined for register."
        sys.exit(1);

    reg = Register(parent, register, register['name'])

#    print reg.__dict__

    reg.index = index

    parent.nodes.append(reg)
    registers.append(reg)
    nodes[reg.prefix_name] = reg
#    print "R",reg.prefix_name,reg.full_name,reg.name

    reg.address = address

    # handle bitfields
    generate_bitfields(reg)

    step = reg.step if reg.step != None else 0x010
    address += step

    return reg, address


def generate_node(parent, config, group_name, registers, nodes, address=0x0000, number=None, index=None):
    """Generate a dictionary of output data to be passed to jinja2"""

    if group_name not in config:
        print "ERROR group",group_name,"not defined."
        sys.exit(1);

    if index == None:
        node = Group(parent, config[group_name], group_name)
    else:
        node = Sequence(parent, config[group_name], group_name, number, index)

#    print node.__dict__

    # link up
    if parent != None: parent.nodes.append(node)
    node.nodes = []
    nodes[node.full_name] = node
#    print "N",node.full_name

    # add offset to base and use as offset
    node.address = address
    if hasattr(node,'offset'): address += node.offset

    # go over entries in group
    first = True
    for entry in node.entries:

        # add offset to address and use as address
        if 'offset' in entry: address = (node.address + entry['offset'])

        if 'ref' in entry:
            # reference to other group
            if 'number' in entry:
                # multiple instantiations of group
                number = entry['number']
                for i in range(number):
                    subnode, address = generate_node(node, config, entry['ref'], registers, nodes, address, number, i)
            else:
                # single reference
                subnode, address = generate_node(node, config, entry['ref'], registers, nodes, address)
        else:
            # register definition
            reg, address = generate_register(node, entry, registers, nodes, address, index)

    return node, address

def print_tree(node, indent = ""):
    print indent,node.name
    for item in node.nodes:
        print_tree(item, indent+"  ")

def print_registers(registers):
    for register in registers:
        print register.name,"@","0x0"+format(register.address,'x'),"(",format(register.offset,'x'),")"

def print_bitfields(registers):
    for register in registers:
        for bf in register.bitfield:
            print bf.full_name,"@","0x0"+format(register.address,'x'),"[",bf.hi,",",bf.lo,"]"

def _vhdl_constant(value, bits=1):
    if bits <= 0:
        # any
        bits = 1;

    if bits%4 == 0:
        hex_digits = bits/4
        fmtstring = 'x"{0:0'+str(bits/4)+'x}"'
        return fmtstring.format(value)
    else:
        fmtstring = '"{0:0'+str(bits)+'b}"'
        return fmtstring.format(value)

def _version(value):
    v = value.split('.')
    return int(v[0])*0x100+int(v[1])

def _append(value, postfix):
    return value+postfix

def _prepend(value, prefix):
    return prefix+value

def _vhdl_logic_vector(bitfield):
        return 'std_logic_vector'+_vhdl_downto(bitfield)

def _vhdl_downto(bitfield):
    if (bitfield.hi < bitfield.lo):
        # any
        return '(64 downto 64)'
    else:
        return '('+str(bitfield.hi)+' downto '+str(bitfield.lo)+')'

def _vhdl_value(bitfield, prefix):
    if bitfield.is_trigger:
        return bitfield.value if isinstance(bitfield.value, basestring) else _vhdl_constant(bitfield.value)
    else:
        return prefix+_vhdl_downto(bitfield)

def _line_comment(value, prefix, indent=0):
    t = "";
    if value != None:
        list = value.split('\n')
        for i,s in enumerate(list):
            if i > 0: t += "\n"+"".rjust(indent," ")
            if s != "" or i < len(list)-1:
                t += prefix + " " + s
    return t;

def _multi_line_comment(value, prefix, postfix, indent=0):
    t = prefix;
    if value != None:
        list = value.split('\n')
        for i,s in enumerate(list):
            t += "\n"
            if s != "" or i < len(list)-1:
                t += "".rjust(indent+len(prefix)," ") + s
    t += postfix
    return t;

def _vhdl_comment(value, indent=0):
    value = value.replace('\#', '#')
    return _line_comment(value, "--", indent)

def _html_comment(value, indent=0):
    value = value.replace('\#', '#')
    return _multi_line_comment(value, "<!--", "-->", indent)

def _tex_comment(value, indent=0):
    value = value.replace('\#', '#')
    return _line_comment(value, "%", indent)

def _c_comment(value, indent=0):
    value = value.replace('\#', '#')
    return _line_comment(value, "// ", indent)

def _html_string(value):
    if value != None and isinstance(value, basestring):
        value = value.replace('\#', '#')
        value = value.replace('\n','<br/>')
    return value

def _c_string(value):
    value = value.replace('\#', '#')
    value = value.replace('\n','\\n')
    return value

def _c_mask(bitfield):
    return ((1 << (bitfield.hi - bitfield.lo + 1)) - 1) << bitfield.lo

def _tex_string(value):
    value = value.replace('\#', '#')
    value = _tex_escape(value)
    value = value.replace('\n','\\newline ')
    return value

def _hex(value, digits=4):
    return ('0x{0:0'+str(digits)+'X}').format(value)

def _semi(field, semi = True):
    return field+(';' if semi else '')

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

def _tex_escape(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

LATEX_YAML_SUBS= (
    (re.compile(r'{%'), r'((*'),
    (re.compile(r'%}'), r'*))'),
    (re.compile(r'{{'), r'((('),
    (re.compile(r'}}'), r')))'),
    (re.compile(r'{#'), r'((='),
    (re.compile(r'#}'), r'=))'),
)

def _tex_yaml_encode(value):
    newval = value
    for pattern, replacement in LATEX_YAML_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

def _camel_case_to_space(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)

def _inc(value, inc = 1):
    return value+inc

def _dec(value, dec = 1):
    return value-dec

def _in_group(node, name):
    if node.name == name:
        return True
    else:
        if node.parent == None:
            return False
        else:
            return _in_group(node.parent, name)

def _list_nodes_recursively(node, doc=False, list=None):
    if list is None:
        list = []

    list.append(node)

    if hasattr(node,'nodes'):
        for item in node.nodes :
            if doc and item.is_sequence and item.index > 0 and item.index < item.number-1:
                if item.index == 1:
                    list.append(Group(node, { }, "..."))
            else:
                _list_nodes_recursively(item, doc, list)
    return list

def generate_output(output, template_file, data):
    """Generate output using the given jinja2 template."""

    env = jinja2.Environment(loader=FileLoader('.'), trim_blocks=True)

    # filters
    env.filters['vhdl_constant'] = _vhdl_constant
    env.filters['vhdl_logic_vector'] = _vhdl_logic_vector
    env.filters['vhdl_downto'] = _vhdl_downto
    env.filters['vhdl_value'] = _vhdl_value
    env.filters['vhdl_comment'] = _vhdl_comment
    env.filters['html_comment'] = _html_comment
    env.filters['html_string'] = _html_string
    env.filters['c_comment'] = _c_comment
    env.filters['c_string'] = _c_string
    env.filters['c_mask'] = _c_mask
    env.filters['tex_comment'] = _tex_comment
    env.filters['tex_string'] = _tex_string
    env.filters['tex_escape'] = _tex_escape
    env.filters['tex_yaml_encode'] = _tex_yaml_encode
    env.filters['version'] = _version
    env.filters['hex'] = _hex
    env.filters['semi'] = _semi
    env.filters['camel_case_to_space'] = _camel_case_to_space
    env.filters['inc'] = _inc
    env.filters['dec'] = _dec
    env.filters['append'] = _append
    env.filters['prepend'] = _prepend
    env.filters['list_nodes_recursively'] = _list_nodes_recursively

     # tests
    env.tests['in_group'] = _in_group

    # change codes for LaTeX
    if output.endswith(".tex"):
        env.block_start_string = '((*'
        env.block_end_string = '*))'
        env.variable_start_string = '((('
        env.variable_end_string = ')))'
        env.comment_start_string = '((='
        env.comment_end_string = '=))'

    # replace placeholders in source template from config (which may contain placeholders)
    template = env.get_template(template_file)
    result = template.render(**data)

    # replace placeholders in config (metadata)
    template = env.from_string(result+"\n")
    result = template.render(**data)

    with open(output, 'w') as f:
        f.write(result.encode('utf-8'))

def diff(diff_file, registers, nodes, data):
    diff_config = read_input(diff_file)
    diff_registers = []
    diff_nodes = {}
    diff_root, diff_offset = generate_node(None, diff_config, "Registers", diff_registers, diff_nodes)

    changed_registers = []

    for register in registers:
        if register.prefix_name in diff_nodes:
            diff_register = diff_nodes[register.prefix_name]

            # equal names, look first into all bitfield changes,
            reg_address_changed = register.address != diff_register.address
            reg_bf_added = False
            reg_bf_removed = False
            reg_bf_incompatible = False
            reg_type_changed = False
            reg_range_changed = False
            reg_desc_changed = False
            reg_value_changed = False

            for bf in register.bitfield:
                if bf.name in diff_register.bitfieldByName:
                    diff_bf = diff_register.bitfieldByName[bf.name]

                    # equal bitfield names
                    type_changed = bf.type != diff_bf.type
                    incompatible = type_changed and (diff_bf.is_write or diff_bf.is_trigger)
                    range_changed = bf.range != diff_bf.range
                    desc_changed = bf.desc != diff_bf.desc
                    value_changed = bf.value != diff_bf.value

                    reg_type_changed = reg_type_changed or type_changed
                    reg_bf_incompatible = reg_bf_incompatible or incompatible
                    reg_range_changed = reg_range_changed or range_changed
                    reg_desc_changed = reg_desc_changed or desc_changed
                    reg_value_changed = reg_value_changed or value_changed

                    bf.type_changed = type_changed
                    bf.range_changed = range_changed
                    bf.desc_changed = desc_changed
                    bf.value_changed = value_changed

                    if type_changed or range_changed or desc_changed:
                        diff_bf.changed = "Changed"
                        bf.changed = "Into"
                    else:
                        diff_bf.changed = ""
                        bf.changed = ""

                else:
                    bf.changed = 'Added'
                    bf.name_changed = True
                    reg_bf_added = True

            for diff_bf in diff_register.bitfield:
                if diff_bf.name not in register.bitfieldByName:
                    diff_bf.changed = 'Removed'
                    reg_bf_removed = True
                    reg_bf_incompatible = True

            if (reg_bf_added or reg_bf_removed or reg_address_changed
                    or reg_range_changed or reg_type_changed or reg_desc_changed
                    or reg_value_changed):
                diff_register.changed = "Changed"
                diff_register.diff_index = (register.address*10)+2
                changed_registers.append(diff_register)

                register.changed = "Into"
                register.address_changed = reg_address_changed
                register.range_changed = reg_range_changed
                register.type_changed = reg_type_changed
                register.desc_changed = reg_desc_changed
                register.value_changed = reg_value_changed
                register.diff_index = (register.address*10)+3
                changed_registers.append(register)

            register.incompatible = (reg_bf_incompatible
                                    or reg_address_changed
                                    or reg_range_changed
                                    or reg_value_changed
                                    or (reg_type_changed and (diff_register.is_write or diff_register.is_trigger)))
            diff_register.incompatible = register.incompatible

    for register in registers:
        if register.prefix_name not in diff_nodes:
            register.changed = 'Added'
            register.incompatible = False
            register.name_changed = True
            register.address_changed = True
            register.range_changed = True
            register.type_changed = True
            register.desc_changed = True
            register.diff_index = (register.address*10)+4
            changed_registers.append(register)

    for diff_register in diff_registers:
        if diff_register.prefix_name not in nodes:
            diff_register.changed = 'Removed'
            diff_register.incompatible = True
            diff_register.diff_index = (diff_register.address*10)+1
            changed_registers.append(diff_register)

    changed_registers = sorted(changed_registers, key=attrgetter('diff_index'))

    sequence = 0
    for register in changed_registers:
        register.sequence = sequence
        if register.changed != "Changed":
            sequence = sequence + 1

    data.update({
        "diff_tree": diff_root,
        "diff_registers": diff_registers,
        "diff_nodes": diff_nodes,
        "changed_registers": changed_registers
    })

def main():
    parser = argparse.ArgumentParser(prog="wuppercodegen", description="Converts template using register map description")
    parser.add_argument("config_file", help="YAML file containing the register map configuration description.")
    parser.add_argument("template_file", help="Jinja2 template file.")
    parser.add_argument("output_file", help="Output file.")
    parser.add_argument('--version', action='version', version='%(prog)s '+__version__)
    parser.add_argument("--diff", dest="diff_file", metavar="YAML file", help="YAML file to compare against.")
#    parser.add_argument("-s", "--address_size", type=int, default=16, help="Enter the address size")
    args = parser.parse_args()

    metadata = {
        "version": __version__,
        "name": "wuppercodegen",
        "exec": sys.argv[0],
        "config": args.config_file,
        "diff": args.diff_file,
        "template": args.template_file,
        "output": args.output_file,
        "cmdline": " ".join(sys.argv)
    }

    config = read_input(args.config_file)

    registers = []
    nodes = {}
    root, offset = generate_node(None, config, "Registers", registers, nodes)
    data = {
        "metadata": metadata,
        "tree": root,
        "registers": registers,
        "nodes": nodes
    }

    if args.diff_file is not None:
        diff(args.diff_file, registers, nodes, data)

    generate_output(args.output_file, args.template_file, data)

#    print_bitfields(registers)

#    print_tree(nodes['Bar0'])

#    for name,node in nodes.iteritems():
#        print name

if __name__ == '__main__':
    main()
