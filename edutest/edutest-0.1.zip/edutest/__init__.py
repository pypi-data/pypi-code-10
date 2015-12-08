from edutest.utils import *
import os.path
import types
import importlib
import edutest.contexts 
from edutest.contexts import ForbiddenInputError

CANT_FIND_FUNCTION="Can't find function {name}"
CANT_IMPORT_MODULE_WITH_INPUT="Can't import {file} as module, because it tried to read input"

_testable_script = None

def get_testable_script():
    if _testable_script is None:
        # TODO: try to detect the module from available files
        raise RuntimeError("Testable module is not set")
    else:
        return _testable_script

def set_testable_script(path):
    global _testable_script
    _testable_script = path

def import_module(name, package=None):
    """Works like :func:`importlib.import_module` but throws error instead of blocking
    when module tries to read from stdin.
    """
    try:
        with edutest.contexts.ForbiddenInput:
            return importlib.import_module(name, package)
    except ForbiddenInputError:
        raise ImportError(CANT_IMPORT_MODULE_WITH_INPUT)

def get_function(name, scope=None):
    """Tries to locate given function ..."""
    assert isinstance(name, str)
    
    if scope is None:
        if "." in name:
            scope, name = name.rsplit(".", maxsplit=1)
        else:
            scope = get_testable_script()
    
    if isinstance(scope, str):
        scope = import_module(scope)
    
    if isinstance(scope, types.ModuleType):
        scope = vars(scope)
    
    assert isinstance(scope, dict)
    assert name in scope, CANT_FIND_FUNCTION.format(name=name)
    return scope[name]

def check_function(
     name_or_object,
     arguments=[],
     expected_result=None,
     inputs=[],
     expected_output=""):
    
    if isinstance(name_or_object, str):
        if "." in name_or_object:
            module_name, function_name = name_or_object.rsplit(".", maxsplit=1)
            module = importlib.import_module(module_name)
            assert hasattr(module, function_name), CANT_FIND_FUNCTION.format(name=name_or_object)
             



# def test_function(
#     name,
#     arguments,
#     expected_result,
#     expected_output="")
# 
# class BasicIOTester:
#     def create_environment_description    
# 
#     def test_io(
#         script_name=None,
#         arguments=[],
#         provided_files={},
#         inputs=[],
#         expected_output=None, 
#         expected_last_output=None, 
#         expected_files={},
#         text_file_encoding="UTF-8"
#         ):
#         
#         if script_name is None:
#             script_name = infer_script_name()
#         
#         instance = ScriptInstance(script_name)
#         try:
#             try:
#                 instance.run(arguments, provided_files, inputs)
#             except:
#                 raise 
#                     
#         finally:
#             # delete files
#             for path in provided_files.keys().union(expected_files.keys()):
#                 if os.path.exists(path):
#                     os.remove(path) 
# 
#     def infer_script_name():
#         return None
# 
# def generate_io_test(
#     script_name=None, # taken from argv
#     arguments=[],
#     inputs=["sisendid"],
#     expected_output=oodatav_väljund, # None, kui ei soovi väljundit kontrollida
#     expected_trimmed_output=None,
#     output_strictness="trim",
#     provided_files={"filename.txt" : "content"},
#     expected_files={"filename.txt" : "content"},
#     description=None,
#     ):
#     pass
# 

def get_solution_file():
    "TODO: inspect filenames in stack and try to find solution file"

