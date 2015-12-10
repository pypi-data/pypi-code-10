# global status, whether to perform type checking
# by default, do nothing (to preserve cpu time)
#
# 0 pass (default)
# 1 warn
# 2 error
status = 0 # by default, pass

'''
disable checktype
'''
def disable():
  global status
  status = 0

'''
configure checktype to print out warnings
def use_warn():
  status = 1
'''

'''
configure checktype to emmit errors
'''
def use_strict():
  global status
  status = 2


class CheckTypeException(Exception):
    pass


def checktype(o, spec):
  if status != 0: # by default, pass
    try:
      spec_o = eval(spec
        .replace('...', '. ..') # to handle [1...] cases
        .replace('..', ',".."')
        .replace('?',  '"?"')
      )
    except:
      raise CheckTypeException('could not parse spec {}'.format(spec))
    _check(o, spec_o, o, spec)


def _check(o, spec, o_original, spec_original):
  #print '_check: o=', o, 'spec=', spec

  if spec != "?": # bypass check if spec is '?'

    # check type equality
    if type(o) != type(spec):
      raise CheckTypeException("Type of '{}' must be of type {} (object: '{}'; spec: '{}')".format(o, type(spec), o_original, spec_original))

    # data structures
    elif type(o) is tuple or type(o) is list:

      if len(spec) > 1 and spec[1] == '..': # is spec of type 1.. ?
        # --> repeat spec[0] for every item of o
        [_check(x, spec[0], o_original, spec_original) for i, x in enumerate(o)]
      else:
        [_check(x, spec[i], o_original, spec_original) for i, x in enumerate(o)]

    elif type(o) is dict:
      assert len(spec) == 1, 'spec {} for dict should only contain 1 single item, e.g. "{{1: \'s\'}}"'.format(spec_original)
      key_spec, value_spec = spec.popitem()
      for key, value in o.items():
        _check(key,   key_spec, o_original, spec_original)
        _check(value, value_spec, o_original, spec_original)

    elif type(o) is set:
      assert len(spec) == 1, 'spec {} for set should only contain 1 single item, e.g. "{{1}}"'.format(spec_original)
      set_spec = spec.pop() # the single item in this set spec
      for i in o:
        _check(i, set_spec, o_original, spec_original)
