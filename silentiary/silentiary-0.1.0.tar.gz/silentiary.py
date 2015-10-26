#!/usr/bin/env python3
"""Silentiary.

Usage:
  silentiary initialize
  silentiary list [<location>] [-r]
  silentiary write [<location>] [<attribute>] [<value>] [-d] [-m]
  silentiary generate [<location>] [<attribute>] [-c CHARSET]... [-l LENGTH]
  silentiary copy [<location>] [<attribute>]
  silentiary type [<location>] [<attribute>]
  silentiary open [<location>] [<attribute>]
  silentiary read [<location>] [<attribute>]
  silentiary delete [<location>] [-r]
  silentiary sync

Options:
  -h --help                    Show this screen.
  -v --version                 Show version.
  -d --display-entry           Echo secret entry to the console.
  -m --multiline               Enter multiple lines of text.
  -r --recursive               Recurse all child locations.
  -c CHARSET --chars=CHARSET   Define character set used in generation
                               [default: ascii_letters digits punctuation].
  -l LENGTH --length=LENGTH    Define length to generate [default: 25].

A location is a string representing a bucket which can hold a number of
  attribute values. When separated by slashes, a heirarchiy is formed.

The attributes used by Silentiary are "password" and "url". Any number of custom
  user defined attributes can additionally take values.

Valid CHARSET names are the python string constants:
  https://docs.python.org/2/library/string.html#string-constants

"""
import subprocess
import json
import webbrowser
import string
import random
import getpass
import os
import errno
import sys
import uuid

from docopt import docopt

HOME = os.path.expanduser('~/.silentiary/')
CONFIG_FILE = 'config.json'
STRUCTURE_FILE = 'structure.json.gpg'
PASSWORD_DIR = 'passwords/'


def get_gpg_command(with_default=True):
    """Get the gpg command list, optionally specifying the default key."""
    command = ['gpg2', '--quiet', '--no-tty', '--default-recipient-self']
    if with_default:
        config = get_config_dict()
        command.extend(['--default-key', config['default-key']])
    return command

def encrypt_content(content, recipients=None):
    """Encrypt the content text, optionally additional recipients."""
    if recipients is None:
        recipients = []
    command = get_gpg_command()
    command.extend(['--encrypt', '--sign', '--armor'])
    for recipient in recipients:
        command.extend(['--recipient', recipient])
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    output = p.communicate(input=content.encode('utf-8'))[0]
    if p.returncode != 0:
        raise Exception('Error encrypting content')
    return output.decode()

def decrypt_content(content):
    """Decrypt content and verify a valid signature exists."""
    r_status, w_status = os.pipe()
    r_log, w_log = os.pipe()
    r_att, w_att = os.pipe()

    command = get_gpg_command()
    command.extend(['--decrypt', '--status-fd', str(w_status),
                    '--logger-fd', str(w_log), '--attribute-fd', str(w_att)])
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                        pass_fds=[w_status, w_log, w_att])
    output = p.communicate(input=content.encode('utf-8'))[0]
    if p.returncode != 0:
        raise Exception('Error decrypting content')

    os.close(w_status)
    os.close(w_log)
    os.close(w_att)

    config = get_config_dict()
    messages = os.fdopen(r_status).read()
    if not (' VALIDSIG ' + config['default-key']) in messages:
        raise Exception('No valid signature from default key')

    return output.decode()

def type_text(text):
    """Alt-Tab and type the selected text."""
    cmd = 'str '+text
    command = ['xte', 'keydown Alt_L', 'key Tab', 'keyup Alt_L',
                'usleep 100000', cmd]
    p = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    p.wait()

def open_url(url):
    """Open a url with the default browser."""
    webbrowser.open(url, new=2, autoraise=True)

def copy_to_clipboard(the_text):
    """Copy the text to the system clipboard."""
    p = subprocess.Popen(['xsel', '--input', '--clipboard'],
                        stdout=subprocess.DEVNULL, stdin=subprocess.PIPE)
    p.communicate(input=the_text.encode('utf-8'))

def generate_password(characters, length):
    """Generate a random password of specified length, using the characters"""
    password = ''
    for i in range(length):
        password = password + random.SystemRandom().choice(characters)
    return password

def split_location(location):
    """Split a location into the heirarchical parts."""
    if location is None:
        return []

    parts = []
    current = ''
    i = 0
    while i < len(location):
        c = location[i]
        if c is '/' and i + 1 < len(location) and location[i+1] is '/':
            current += '/'
            i += 2
        elif c is '/':
            if len(current) > 0:
                parts.append(current)
            current = ''
            i += 1
        else:
            current += c
            i += 1
    if len(current) > 0:
        parts.append(current)
    return parts

def get_user_input(prompt, echo=True, multiline=False):
    """Get user input from standard in. Optionally echo to screen and multiline."""
    to_return = ''
    if echo:
        to_return = input(prompt)
    else:
        to_return = getpass.getpass(prompt)
    while multiline:
        try:
            to_return += '\n' + get_user_input('', echo, False)
        except EOFError:
            return to_return
    return to_return

def get_input_with_default(prompt, default_value):
    """Get user input and indicate the default value if no entry made."""
    if default_value is not None:
        prompt = prompt + '[' + default_value + ']'
    prompt = prompt + ': '
    value = get_user_input(prompt)
    if value is '':
        return default_value
    return value

def verify_location_input(input_value):
    location_string = input_value
    if not location_string:
        location_string = get_input_with_default("Location", "/")
    return location_string

def verify_attribute_input(input_value, default_value):
    attribute_string = input_value
    if not input_value:
        attribute_string = get_input_with_default("Attribute", default_value)
    return attribute_string

def get_file_content(file_path):
    """Get file contents relative to the HOME directory."""
    file_path = HOME + file_path
    if not os.path.isfile(file_path):
        raise OSError(errno.ENOENT, 'No such file', file_path)
    if not os.access(file_path, os.R_OK):
        raise OSError(errno.EACCES, 'Permission denied', file_path)
    f = open(file_path, 'r')
    return f.read()

def get_config_dict():
    """Load the configuration dictionary."""
    is_new_file = False
    try:
        txt = get_file_content(CONFIG_FILE)
    except OSError as e:
        is_new_file = True
        if e.errno != errno.ENOENT:
            raise
    if not is_new_file:
        return json.loads(txt)
    return {}

def get_encrypted_json(file_path):
    """Load and decrypt the indicated json file."""
    is_new_file = False
    try:
        encrypted = get_file_content(file_path)
    except OSError as e:
        is_new_file = True
        if e.errno != errno.ENOENT:
            raise
    if not is_new_file:
        decrypted = decrypt_content(encrypted)
        return json.loads(decrypted)
    return {}

def put_file_content(file_path, content):
    """Write file contents relative to the HOME directory."""
    file_path = HOME + file_path
    f = open(file_path, 'w')
    f.write(content)

def put_encrypted_json(file_path, dict_content):
    """Encrypt a dictionary, and write it to the file path."""
    content = json.dumps(dict_content, indent=4)
    encrypted = encrypt_content(content)
    put_file_content(file_path, encrypted)

def add_attribute_to_structure(location, attribute, value):
    """Add this value into the encrypted data structure."""
    structure = get_encrypted_json(STRUCTURE_FILE)
    if 'children' not in structure:
        structure['uid'] = str(uuid.uuid1())
        structure['children'] = {}
    position = structure
    for pos in location:
        if pos not in position['children']:
            position['children'][pos] = {'uid':str(uuid.uuid1()), 'children':{}}
        position = position['children'][pos]
    put_encrypted_json(STRUCTURE_FILE, structure)

    file_path = PASSWORD_DIR + position['uid'] + '.json.gpg'
    data = get_encrypted_json(file_path)
    if 'values' not in data:
        data['location'] = location
        data['values'] = {}
    data['values'][attribute] = value
    put_encrypted_json(file_path, data)

def get_all_attributes(location):
    """Read a value from the encrypted data structure."""
    position = get_encrypted_json(STRUCTURE_FILE)
    for pos in location:
        position = position['children'][pos]

    file_path = PASSWORD_DIR + position['uid'] + '.json.gpg'
    data = get_encrypted_json(file_path)
    return data['values']

def get_attribute_from_structure(location, attribute):
    """Read a value from the encrypted data structure."""
    return get_all_attributes(location)[attribute]

def delete_attribute_from_structure(location, attribute):
    """Delete an attribute from the encrypted data structure."""
    position = get_encrypted_json(STRUCTURE_FILE)
    for pos in location:
        position = position['children'][pos]

    file_path = PASSWORD_DIR + position['uid'] + '.json.gpg'
    data = get_encrypted_json(file_path)
    del data['values'][attribute]
    put_encrypted_json(file_path, data)

def delete_location_from_structure(location, is_recursive):
    """Delete a location from the encrypted data structure, optionally recursive."""
    target = location.pop()
    structure = get_encrypted_json(STRUCTURE_FILE)
    position = structure
    for pos in location:
        position = position['children'][pos]

    if position['children'][target]['children'] and not is_recursive:
        raise Exception("Location has children and delete is not recursive")

    recursive_remove_json(position['children'][target], is_recursive)

    del position['children'][target]
    put_encrypted_json(STRUCTURE_FILE, structure)

def recursive_remove_json(target, is_recursive):
    """Delete the encrypted password storage files, optionally recursive."""
    if is_recursive and target['children']:
        for child in target['children'].items():
            recursive_remove_json(child[1], is_recursive)
    filename = HOME + PASSWORD_DIR + target['uid'] + '.json.gpg'
    if os.path.isfile(filename):
        os.remove(filename)

def print_structure(structure, depth, enddepth, recursive):
    """List the groups in the encrypted data structure, optionally recursive."""
    if 'children' in structure and structure['children']:
        keys = sorted(structure['children'].keys())
        last_key = keys.pop()
        for key in keys:
            print_at_depth(depth, False, enddepth, key)
            if recursive and 'children' in structure['children'][key]:
                print_structure(structure['children'][key], depth+1,
                                enddepth, recursive)
        print_at_depth(depth, True, enddepth, last_key)
        if recursive and 'children' in structure['children'][last_key]:
            print_structure(structure['children'][last_key], depth+1,
                            enddepth+1, recursive)

def print_at_depth(depth, lastkey, enddepth, value):
    output = (depth-enddepth)*'|   '
    output += enddepth*'    '
    if lastkey:
        output += '`'
    else:
        output += '|'
    output += '-- ' + value
    print(output)

def print_all_attributes(location):
    attributes = get_all_attributes(location)
    for key in sorted(attributes.keys()):
        if '\n' in attributes[key]:
            print('---------- '+key+' ----------')
            print(attributes[key])
            print(20*'-'+ ((len(key)+2)*'-'))
        else:
            print(key+': '+attributes[key])

# Action Functions:
def action_initialize():
    if not os.path.exists(HOME + PASSWORD_DIR):
        os.makedirs(HOME + PASSWORD_DIR)
    config = get_config_dict()

    key = None
    if 'default-key' in config:
        key = config['default-key']
    key = get_input_with_default('Default Key', key).replace(" ", "")

    command = get_gpg_command(with_default=False)
    command.extend(['--list-keys', key])
    p = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    p.wait()
    if p.returncode != 0:
        raise LookupError(key, 'Key not found')

    config['default-key'] = key
    put_file_content(CONFIG_FILE, json.dumps(config, indent=4))

def action_list(location_string, recursive):
    location = split_location(verify_location_input(location_string))
    position = get_encrypted_json(STRUCTURE_FILE)
    for pos in location:
        position = position['children'][pos]
    print_structure(position, 0, 0, recursive)

def action_write(location_string, attribute, value, is_visible, is_multiline):
    location = split_location(verify_location_input(location_string))
    attribute = verify_attribute_input(attribute, "password")
    if not value:
        value = get_user_input('Attribute Value: ', is_visible, is_multiline)
    if value in ('', None):
        delete_attribute_from_structure(location, attribute)
    else:
        add_attribute_to_structure(location, attribute, value)

def action_generate(location_string, attribute, charset, length):
    location = split_location(verify_location_input(location_string))
    attribute = verify_attribute_input(attribute, "password")
    characters = ''
    for name in charset:
        characters += getattr(string, name)
    if len(characters) is 0:
        raise ValueError('Attempt to generate password with no charset')
    value = generate_password(characters, length)
    add_attribute_to_structure(location, attribute, value)

def action_copy(location_string, attribute):
    location = split_location(verify_location_input(location_string))
    attribute = verify_attribute_input(attribute, "password")
    copy_to_clipboard(get_attribute_from_structure(location, attribute))

def action_open(location_string, attribute):
    location = split_location(verify_location_input(location_string))
    attribute = verify_attribute_input(attribute, "url")
    open_url(get_attribute_from_structure(location, attribute))

def action_read(location_string, attribute):
    location = split_location(verify_location_input(location_string))
    attribute = get_user_input("Attibute [ALL]: ")
    if attribute:
        print(get_attribute_from_structure(location, attribute))
    else:
        print_all_attributes(location)

def action_type(location_string, attribute):
    location = split_location(verify_location_input(location_string))
    if not attribute:
        attribute = get_input_with_default("Attribute", "password")
    type_text(get_attribute_from_structure(location, attribute))

def action_delete(location_string, is_recursive):
    location = split_location(verify_location_input(location_string))
    if not location:
        raise ValueError('Can not delete root location')
    delete_location_from_structure(location, is_recursive)

def action_sync():
    #git add -A *.gpg ; git commit -m "auto"
    #git pull -Xours
    #git push
    print('todo: sync')

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Silentiary 0.1.0')

    if arguments['initialize']:
        action_initialize()
        sys.exit()

    if arguments['list']:
        action_list(arguments['<location>'], arguments['--recursive'])

    elif arguments['write']:
        action_write(arguments['<location>'], arguments['<attribute>'],
                        arguments['<value>'], arguments['--display-entry'],
                        arguments['--multiline'])

    elif arguments['generate']:
        action_generate(arguments['<location>'], arguments['<attribute>'],
                        arguments['--chars'], int(arguments['--length']))

    elif arguments['copy']:
        action_copy(arguments['<location>'], arguments['<attribute>'])

    elif arguments['open']:
        action_open(arguments['<location>'], arguments['<attribute>'])

    elif arguments['read']:
        action_read(arguments['<location>'], arguments['<attribute>'])

    elif arguments['type']:
        action_type(arguments['<location>'], arguments['<attribute>'])

    elif arguments['delete']:
        action_delete(arguments['<location>'], arguments['--recursive'])

    elif arguments['sync']:
        action_sync()
