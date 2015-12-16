import re
# global status, whether to perform type checking
# by default, do nothing (to preserve cpu time)
checktype_active = False # by default, pass

'''
disable checktype (default)
'''
def disable_checktype():
  global checktype_active
  checktype_active = False

'''
configure checktype to emmit errors
'''
def activate_checktype():
  global checktype_active
  checktype_active = True


class CheckTypeException(Exception):
    pass

valid_spec = re.compile(r'^(int|str|float|bool|self|None|[,\.: \?\{\}\[\]\(\)])+$').match
# removes all named variables (letters, numbers and _-)
remove_named_vars = re.compile(r'[a-z_\-0-9]+@').sub

'''
main function to check the type of the provided object, given a spec
'''
def checktype(obj, spec, bypass=False):
  if checktype_active or bypass: # by default, pass

    spec_novars = remove_named_vars('', spec)

    if not valid_spec(spec_novars):
      raise CheckTypeException('spec can only contain int, float, str, bool, self, None and a combination of ,.: ?{{}}[]() but was >>{}<<'.format(spec))

    # transform the spec from [(int,str)..] to [(1,'m'), '..']
    spec_p = str(spec_novars)\
      .replace('int',   '1')\
      .replace('float', '1.0')\
      .replace('str',   '"m"')\
      .replace('bool',  'True')\
      .replace('?',     '"ignore"')\
      .replace('self',  '"ignore"')\
      .replace('..', ',".."')
    #print 'spec_p >{}<'.format(spec_p)

    try:
      spec_o = eval(spec_p)
    except:
      raise CheckTypeException('could not parse spec >>{}<< (resolved to >>{}<<)'.format(spec, spec_p))
    _check(obj, spec_o, obj, spec)


def _check(o, spec, o_original, spec_original):
  #print '_check: obj=', o, 'spec=', spec

  if spec != "ignore": # bypass check if spec is wildcard ('?', self, None)

    # check type equality
    if type(o) is set and str(spec) == '{}':  # exception for empty set
      pass                                    # (else its eval is considered a dict)
    elif type(o) != type(spec):
      raise CheckTypeException("Type of '{}' must be of type {} (object: '{}'; spec: '{}')".format(o, type(spec), o_original, spec_original))

    # handle data structures recursively
    elif type(o) is tuple or type(o) is list:

      if len(spec) == 0: # empty spec, e.g. () or [] -> ignore (type equivalence was already tested above)
        pass

      elif len(spec) == 2 and spec[1] == '..': # spec of type dotdot (e.g. int..)
        # --> repeat spec[0] for every item of o
        [_check(x, spec[0], o_original, spec_original) for i, x in enumerate(o)]

      else: # spec is fixed length, e.g. [int,int,float,str]

        for s in spec: # check that spec does not contain ..
          if s == '..':
            raise CheckTypeException('Illegal spec {}; can only contain .. at the second entry of a tuple or list, e.g. [int..] or [str..]'.format(spec_original))

        if len(spec) != len(o):
          raise CheckTypeException("Object length of {} does not match spec {} (object: '{}'; spec: '{}')".format(o, spec, o_original, spec_original))


        [_check(x, spec[i], o_original, spec_original) for i, x in enumerate(o)]

    elif type(o) is dict:
      if len(spec) == 0: # empty spec {} -> ignore
        pass
      elif len(spec) == 1:
        key_spec, value_spec = spec.popitem()
        for key, value in o.items():
          _check(key,   key_spec, o_original, spec_original)
          _check(value, value_spec, o_original, spec_original)
      else:
        raise CheckTypeException('Spec {} for dict should only contain 1 single item, e.g. "{{1: \'s\'}}"'.format(spec_original))

    elif type(o) is set:
      assert len(spec) == 1, 'spec {} for set should only contain 1 single item, e.g. "{{1}}"'.format(spec_original)
      set_spec = spec.pop() # the single item in this set spec
      for i in o:
        _check(i, set_spec, o_original, spec_original)

'''
Decorator; usage:

@check('str, {str:int} -> [int..]')
    def myfunction(a1, a2):
        return [1,2,3]

myfunction("say", {"hello":1})
'''
class check(object):
  spec_in, spec_out = None, None

  def __init__(self, spec):
      if '->' in spec: # beware it can be int->int, ->int, int->
          (self.spec_in, self.spec_out) = spec.split('->')
      else: # a single arg, let's consider it's the input spec
          self.spec_in = spec
      #print 'self.spec_in', self.spec_in, 'self.spec_out', self.spec_out

  def __call__(self, fn):
      def wrapped_fn(*args):
          if self.spec_in is not None:
            checktype(args, spec=self.spec_in)
          return fn(*args)
          if self.spec_out is not None:
              checktype(out, self.spec_out)
      return wrapped_fn
