import re
import ast
import traceback
import sys
import locale

def get_source(path):
    import tokenize
    # encoding-safe open
    with tokenize.open(path) as sourceFile:
        contents = sourceFile.read()
    return contents

def is_function(value):
    try:
        return hasattr(value, '__call__')
    except:
        return False

def get_error_message(exception=None):
    if exception:
        type_ = type(exception)
        msg = str(exception)
    else:
        type_, msg, _ = sys.exc_info()
         
    return "{}: {}".format(type_.__name__, msg)


def get_traceback(exception):
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))



def quote_text_block(text):
    return "\n>" + text.replace("\n", "\n>")

def extract_numbers(s, allow_decimal_comma=False):
    result = []
    
    if allow_decimal_comma:
        rexp = """((?:\+|\-)?\d+(?:(?:\.|,)\d+)?)"""
    else:
        rexp = """((?:\+|\-)?\d+(?:\.\d+)?)"""
        
    for item in re.findall(rexp, s):
        try:
            result.append(int(item))
        except:
            try:
                result.append(float(item.replace(",", ".")))
            except:
                pass
    return result

def contains_number(num_list_or_str, x, allowed_error=0, allow_decimal_comma=False):
    if isinstance(num_list_or_str, str):
        nums = extract_numbers(num_list_or_str, allow_decimal_comma)
    else:
        nums = num_list_or_str
    
    for num in nums:
        if abs(num - x) <= allowed_error:
            return True
    
    return False

def ast_contains_name(node, name):
    if isinstance(node, ast.Name) and node.id == name:
        return True
    
    for child in ast.iter_child_nodes(node):
        if ast_contains_name(child, name):
            return True

    return False

def ast_contains(node, node_type):
    if isinstance(node, node_type):
        return True
    
    for child in ast.iter_child_nodes(node):
        if ast_contains(child, node_type):
            return True

    return False

def create_file(path, content, text_file_encoding=None):
    if text_file_encoding is None:
        text_file_encoding = locale.getpreferredencoding(False)
    
    if isinstance(content, str):
        content = content.encode(text_file_encoding)
        
    with open(path, mode="wb") as fp:
        fp.write(content)
    