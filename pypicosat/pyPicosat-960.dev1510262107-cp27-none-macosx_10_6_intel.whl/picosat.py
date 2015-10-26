# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.7
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_picosat', [dirname(__file__)])
        except ImportError:
            import _picosat
            return _picosat
        if fp is not None:
            try:
                _mod = imp.load_module('_picosat', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _picosat = swig_import_helper()
    del swig_import_helper
else:
    import _picosat
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



_picosat.PICOSAT_API_VERSION_swigconstant(_picosat)
PICOSAT_API_VERSION = _picosat.PICOSAT_API_VERSION

_picosat.PICOSAT_UNKNOWN_swigconstant(_picosat)
PICOSAT_UNKNOWN = _picosat.PICOSAT_UNKNOWN

_picosat.PICOSAT_SATISFIABLE_swigconstant(_picosat)
PICOSAT_SATISFIABLE = _picosat.PICOSAT_SATISFIABLE

_picosat.PICOSAT_UNSATISFIABLE_swigconstant(_picosat)
PICOSAT_UNSATISFIABLE = _picosat.PICOSAT_UNSATISFIABLE

def picosat_version():
    return _picosat.picosat_version()
picosat_version = _picosat.picosat_version

def picosat_config():
    return _picosat.picosat_config()
picosat_config = _picosat.picosat_config

def picosat_copyright():
    return _picosat.picosat_copyright()
picosat_copyright = _picosat.picosat_copyright

def picosat_init():
    return _picosat.picosat_init()
picosat_init = _picosat.picosat_init

def picosat_minit(state, arg2, arg3, arg4):
    return _picosat.picosat_minit(state, arg2, arg3, arg4)
picosat_minit = _picosat.picosat_minit

def picosat_reset(arg1):
    return _picosat.picosat_reset(arg1)
picosat_reset = _picosat.picosat_reset

def picosat_set_output(arg1, arg2):
    return _picosat.picosat_set_output(arg1, arg2)
picosat_set_output = _picosat.picosat_set_output

def picosat_measure_all_calls(arg1):
    return _picosat.picosat_measure_all_calls(arg1)
picosat_measure_all_calls = _picosat.picosat_measure_all_calls

def picosat_set_prefix(arg1, arg2):
    return _picosat.picosat_set_prefix(arg1, arg2)
picosat_set_prefix = _picosat.picosat_set_prefix

def picosat_set_verbosity(arg1, new_verbosity_level):
    return _picosat.picosat_set_verbosity(arg1, new_verbosity_level)
picosat_set_verbosity = _picosat.picosat_set_verbosity

def picosat_set_plain(arg1, new_plain_value):
    return _picosat.picosat_set_plain(arg1, new_plain_value)
picosat_set_plain = _picosat.picosat_set_plain

def picosat_set_global_default_phase(arg1, arg2):
    return _picosat.picosat_set_global_default_phase(arg1, arg2)
picosat_set_global_default_phase = _picosat.picosat_set_global_default_phase

def picosat_set_default_phase_lit(arg1, lit, phase):
    return _picosat.picosat_set_default_phase_lit(arg1, lit, phase)
picosat_set_default_phase_lit = _picosat.picosat_set_default_phase_lit

def picosat_reset_phases(arg1):
    return _picosat.picosat_reset_phases(arg1)
picosat_reset_phases = _picosat.picosat_reset_phases

def picosat_reset_scores(arg1):
    return _picosat.picosat_reset_scores(arg1)
picosat_reset_scores = _picosat.picosat_reset_scores

def picosat_remove_learned(arg1, percentage):
    return _picosat.picosat_remove_learned(arg1, percentage)
picosat_remove_learned = _picosat.picosat_remove_learned

def picosat_set_more_important_lit(arg1, lit):
    return _picosat.picosat_set_more_important_lit(arg1, lit)
picosat_set_more_important_lit = _picosat.picosat_set_more_important_lit

def picosat_set_less_important_lit(arg1, lit):
    return _picosat.picosat_set_less_important_lit(arg1, lit)
picosat_set_less_important_lit = _picosat.picosat_set_less_important_lit

def picosat_message(arg1, verbosity_level, fmt):
    return _picosat.picosat_message(arg1, verbosity_level, fmt)
picosat_message = _picosat.picosat_message

def picosat_set_seed(arg1, random_number_generator_seed):
    return _picosat.picosat_set_seed(arg1, random_number_generator_seed)
picosat_set_seed = _picosat.picosat_set_seed

def picosat_enable_trace_generation(arg1):
    return _picosat.picosat_enable_trace_generation(arg1)
picosat_enable_trace_generation = _picosat.picosat_enable_trace_generation

def picosat_set_incremental_rup_file(arg1, file, m, n):
    return _picosat.picosat_set_incremental_rup_file(arg1, file, m, n)
picosat_set_incremental_rup_file = _picosat.picosat_set_incremental_rup_file

def picosat_save_original_clauses(arg1):
    return _picosat.picosat_save_original_clauses(arg1)
picosat_save_original_clauses = _picosat.picosat_save_original_clauses

def picosat_inc_max_var(arg1):
    return _picosat.picosat_inc_max_var(arg1)
picosat_inc_max_var = _picosat.picosat_inc_max_var

def picosat_push(arg1):
    return _picosat.picosat_push(arg1)
picosat_push = _picosat.picosat_push

def picosat_failed_context(arg1, lit):
    return _picosat.picosat_failed_context(arg1, lit)
picosat_failed_context = _picosat.picosat_failed_context

def picosat_context(arg1):
    return _picosat.picosat_context(arg1)
picosat_context = _picosat.picosat_context

def picosat_pop(arg1):
    return _picosat.picosat_pop(arg1)
picosat_pop = _picosat.picosat_pop

def picosat_simplify(arg1):
    return _picosat.picosat_simplify(arg1)
picosat_simplify = _picosat.picosat_simplify

def picosat_adjust(arg1, max_idx):
    return _picosat.picosat_adjust(arg1, max_idx)
picosat_adjust = _picosat.picosat_adjust

def picosat_variables(arg1):
    return _picosat.picosat_variables(arg1)
picosat_variables = _picosat.picosat_variables

def picosat_added_original_clauses(arg1):
    return _picosat.picosat_added_original_clauses(arg1)
picosat_added_original_clauses = _picosat.picosat_added_original_clauses

def picosat_max_bytes_allocated(arg1):
    return _picosat.picosat_max_bytes_allocated(arg1)
picosat_max_bytes_allocated = _picosat.picosat_max_bytes_allocated

def picosat_time_stamp():
    return _picosat.picosat_time_stamp()
picosat_time_stamp = _picosat.picosat_time_stamp

def picosat_stats(arg1):
    return _picosat.picosat_stats(arg1)
picosat_stats = _picosat.picosat_stats

def picosat_propagations(arg1):
    return _picosat.picosat_propagations(arg1)
picosat_propagations = _picosat.picosat_propagations

def picosat_decisions(arg1):
    return _picosat.picosat_decisions(arg1)
picosat_decisions = _picosat.picosat_decisions

def picosat_visits(arg1):
    return _picosat.picosat_visits(arg1)
picosat_visits = _picosat.picosat_visits

def picosat_seconds(arg1):
    return _picosat.picosat_seconds(arg1)
picosat_seconds = _picosat.picosat_seconds

def picosat_add(arg1, lit):
    return _picosat.picosat_add(arg1, lit)
picosat_add = _picosat.picosat_add

def picosat_add_arg(arg1):
    return _picosat.picosat_add_arg(arg1)
picosat_add_arg = _picosat.picosat_add_arg

def picosat_add_lits(arg1, lits):
    return _picosat.picosat_add_lits(arg1, lits)
picosat_add_lits = _picosat.picosat_add_lits

def picosat_print(arg1, arg2):
    return _picosat.picosat_print(arg1, arg2)
picosat_print = _picosat.picosat_print

def picosat_assume(arg1, lit):
    return _picosat.picosat_assume(arg1, lit)
picosat_assume = _picosat.picosat_assume

def picosat_add_ado_lit(arg1, arg2):
    return _picosat.picosat_add_ado_lit(arg1, arg2)
picosat_add_ado_lit = _picosat.picosat_add_ado_lit

def picosat_sat(arg1, decision_limit):
    return _picosat.picosat_sat(arg1, decision_limit)
picosat_sat = _picosat.picosat_sat

def picosat_set_propagation_limit(arg1, limit):
    return _picosat.picosat_set_propagation_limit(arg1, limit)
picosat_set_propagation_limit = _picosat.picosat_set_propagation_limit

def picosat_res(arg1):
    return _picosat.picosat_res(arg1)
picosat_res = _picosat.picosat_res

def picosat_deref(arg1, lit):
    return _picosat.picosat_deref(arg1, lit)
picosat_deref = _picosat.picosat_deref

def picosat_deref_toplevel(arg1, lit):
    return _picosat.picosat_deref_toplevel(arg1, lit)
picosat_deref_toplevel = _picosat.picosat_deref_toplevel

def picosat_deref_partial(arg1, lit):
    return _picosat.picosat_deref_partial(arg1, lit)
picosat_deref_partial = _picosat.picosat_deref_partial

def picosat_inconsistent(arg1):
    return _picosat.picosat_inconsistent(arg1)
picosat_inconsistent = _picosat.picosat_inconsistent

def picosat_failed_assumption(arg1, lit):
    return _picosat.picosat_failed_assumption(arg1, lit)
picosat_failed_assumption = _picosat.picosat_failed_assumption

def picosat_failed_assumptions(arg1):
    return _picosat.picosat_failed_assumptions(arg1)
picosat_failed_assumptions = _picosat.picosat_failed_assumptions

def picosat_mus_assumptions(arg1, arg2, arg3, arg4):
    return _picosat.picosat_mus_assumptions(arg1, arg2, arg3, arg4)
picosat_mus_assumptions = _picosat.picosat_mus_assumptions

def picosat_maximal_satisfiable_subset_of_assumptions(arg1):
    return _picosat.picosat_maximal_satisfiable_subset_of_assumptions(arg1)
picosat_maximal_satisfiable_subset_of_assumptions = _picosat.picosat_maximal_satisfiable_subset_of_assumptions

def picosat_next_maximal_satisfiable_subset_of_assumptions(arg1):
    return _picosat.picosat_next_maximal_satisfiable_subset_of_assumptions(arg1)
picosat_next_maximal_satisfiable_subset_of_assumptions = _picosat.picosat_next_maximal_satisfiable_subset_of_assumptions

def picosat_next_minimal_correcting_subset_of_assumptions(arg1):
    return _picosat.picosat_next_minimal_correcting_subset_of_assumptions(arg1)
picosat_next_minimal_correcting_subset_of_assumptions = _picosat.picosat_next_minimal_correcting_subset_of_assumptions

def picosat_humus(arg1, callback, state):
    return _picosat.picosat_humus(arg1, callback, state)
picosat_humus = _picosat.picosat_humus

def picosat_changed(arg1):
    return _picosat.picosat_changed(arg1)
picosat_changed = _picosat.picosat_changed

def picosat_coreclause(arg1, i):
    return _picosat.picosat_coreclause(arg1, i)
picosat_coreclause = _picosat.picosat_coreclause

def picosat_corelit(arg1, lit):
    return _picosat.picosat_corelit(arg1, lit)
picosat_corelit = _picosat.picosat_corelit

def picosat_write_clausal_core(arg1, core_file):
    return _picosat.picosat_write_clausal_core(arg1, core_file)
picosat_write_clausal_core = _picosat.picosat_write_clausal_core

def picosat_write_compact_trace(arg1, trace_file):
    return _picosat.picosat_write_compact_trace(arg1, trace_file)
picosat_write_compact_trace = _picosat.picosat_write_compact_trace

def picosat_write_extended_trace(arg1, trace_file):
    return _picosat.picosat_write_extended_trace(arg1, trace_file)
picosat_write_extended_trace = _picosat.picosat_write_extended_trace

def picosat_write_rup_trace(arg1, trace_file):
    return _picosat.picosat_write_rup_trace(arg1, trace_file)
picosat_write_rup_trace = _picosat.picosat_write_rup_trace

def picosat_usedlit(arg1, lit):
    return _picosat.picosat_usedlit(arg1, lit)
picosat_usedlit = _picosat.picosat_usedlit


## EXTRA_PYTHON_CODE_TAG


# This file is compatible with both classic and new-style classes.


