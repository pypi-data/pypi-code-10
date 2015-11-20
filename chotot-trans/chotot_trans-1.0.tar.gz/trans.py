from commands import *
import re
import json
def generate_command(cmd, args={}, commit=True):
    command = "cmd:%s\\n" %cmd
    if isinstance(args, dict):
        for name, arg in args.iteritems():
            command += _build_argument(name, arg)
    elif isinstance(args, list):
        for name, arg in args:
            command += _build_argument(name, arg)
    if commit:
        command += "commit:1\\n"
    command += "end\\n"
    return command

def _build_argument(key, value):
    encode_type = 'latin-1'
    if isinstance(key, unicode):
        key = key.encode(encode_type)

    arg_type = type(value)

    if arg_type == unicode:
        value = value.encode(encode_type)
        arg_type = str

    if arg_type == str and re.search("[\r\n]", value):
        value = {"blob": value}
        arg_type = dict

    if arg_type == dict and value.has_key("blob"):
        blob = value["blob"]
        if isinstance(blob, unicode):
            blob = blob.encode(encode_type)
        return "blob:{}:{}\n{}\n".format(len(blob), key, blob)
    elif arg_type in (list, tuple):
        out = StringIO()
        for item in value:
            if isinstance(item, unicode):
                item = item.encode(encode_type)

            if isinstance(item, str) and re.search("[\r\n]", item):
                out.write("blob:{}:{}\n{}\n".format(len(item), key, item))
            else:
                out.write("{}:{}\n".format(key, str(item)))

        ret = out.getvalue()
        out.close()
        return ret

    if arg_type in (dict, list, tuple):
        return False
    return "%s:%s\\n" % (key, value)

def execute(command, host, port, with_parse=True):
    # get command
    shell_command = 'printf "%s" | nc %s %s' % (command, host, port)
    print shell_command

    trans_output = getoutput(shell_command)

    if not trans_output:
        raise ConnectionError('database does not response, please try again')
    elif trans_output.startswith('nc'):
        raise ConnectionError(trans_output)
    if with_parse:
        return parse(trans_output)
    return trans_output

def parse(trans_ouput):
    try:
        return json.load(trans_ouput)
    except:
        items = trans_ouput.split("\n")
        items = filter(lambda x: x and ":" in x and x != "end", items)
        data = {}
        for x in items:
            if ':' not in x:
                raise ConnectionError('Can not parse trans result', 500)
            parts = x.split(':')
            value = ":".join(parts[1:])
            keys_string = parts[0]
            keys = keys_string.split('.')
            node = data
            for k in keys[:-1]:
                if node.get(k, None) is None:
                    node[k] = {}
                node = node[k]
            node[keys[-1]] = value
        return data
