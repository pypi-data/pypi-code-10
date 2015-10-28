"""
ProbLog command-line interface.

Copyright 2015 KU Leuven, DTAI Research Group

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function

import stat
import sys
import os
import traceback

from ..program import PrologFile
from ..evaluator import SemiringLogProbability, SemiringProbability, SemiringSymbolic
from .. import get_evaluatable, get_evaluatables

from ..util import Timer, start_timer, stop_timer, init_logger, format_dictionary
from ..errors import process_error


def print_result(d, output, precision=8):
    """Pretty print result.

    :param d: result from run_problog
    :param output: output file
    :param precision:
    :return:
    """
    success, d = d
    if success:
        print(format_dictionary(d, precision), file=output)
        return 0
    else:
        print (process_error(d), file=output)
        return 1


def print_result_json(d, output, precision=8):
    """Pretty print result.

    :param d: result from run_problog
    :param output: output file
    :param precision:
    :return:
    """
    import json
    result = {}
    success, d = d
    if success:
        result['SUCCESS'] = True
        result['probs'] = [[str(n), round(p, precision), n.loc[1], n.loc[2]] for n, p in d.items()]
    else:
        result['SUCCESS'] = False
        result['err'] = vars(d)
    print (json.dumps(result), file=output)
    return 0


def execute(filename, knowledge=None, semiring=None, debug=False, **kwdargs):
    """Run ProbLog.

    :param filename: input file
    :param knowledge: knowledge compilation class or identifier
    :param semiring: semiring to use
    :param parse_class: prolog parser to use
    :param debug: enable advanced error output
    :param engine_debug: enable engine debugging output
    :param kwdargs: additional arguments
    :return: tuple where first value indicates success, and second value contains result details
    """

    if knowledge is None or type(knowledge) == str:
        knowledge = get_evaluatable(knowledge)
    try:
        with Timer('Total time'):
            model = PrologFile(filename)
            formula = knowledge.create_from(model, **kwdargs)
            result = formula.evaluate(semiring=semiring, **kwdargs)

            # Update loceation information on result terms
            for n, p in result.items():
                if not n.location or not n.location[0]:
                    # Only get location for primary file (other file information is not available).
                    n.loc = model.lineno(n.location)
        return True, result
    except Exception as err:
        trace = traceback.format_exc()
        err.trace = trace
        return False, err


def argparser():
    """Create the default argument parser for ProbLog.
    :return: argument parser
    :rtype: argparse.ArgumentParser
    """
    import argparse

    class InputFile(str):
        """Stub class for file input arguments."""
        pass

    class OutputFile(str):
        """Stub class for file output arguments."""
        pass

    description = """ProbLog 2.1 command line interface

    The arguments listed below are for the default mode.
    ProbLog also supports the following alternative modes:

      - (default): inference
      - install: run the installer
      - explain: compute the probability of a query and explain how to get there
      - ground: generate ground program (see ground --help)
      - sample: generate samples from the model (see sample --help)
      - unittest: run the testsuite

    Select a mode by adding one of these keywords as first argument (e.g. problog-cli.py install).
    """

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filenames', metavar='MODEL', nargs='*', type=InputFile)
    parser.add_argument('--verbose', '-v', action='count', help='Verbose output')
    parser.add_argument('--knowledge', '-k', dest='koption',
                        choices=get_evaluatables(),
                        default=None, help="Knowledge compilation tool.")

    # Evaluation semiring
    ls_group = parser.add_mutually_exclusive_group()
    ls_group.add_argument('--logspace', action='store_true',
                          help="Use log space evaluation (default).", default=True)
    ls_group.add_argument('--nologspace', dest='logspace', action='store_false',
                          help="Use normal space evaluation.")
    ls_group.add_argument('--symbolic', dest='symbolic', action='store_true',
                          help="Use symbolic computations.")

    parser.add_argument('--output', '-o', help="Output file (default stdout)", type=OutputFile)
    parser.add_argument('--recursion-limit',
                        help="Set Python recursion limit. (default: %d)" % sys.getrecursionlimit(),
                        default=sys.getrecursionlimit(), type=int)
    parser.add_argument('--timeout', '-t', type=int, default=0,
                        help="Set timeout (in seconds, default=off).")
    parser.add_argument('--compile-timeout', type=int, default=0,
                        help="Set timeout for compilation (in seconds, default=off).")
    parser.add_argument('--debug', '-d', action='store_true',
                        help="Enable debug mode (print full errors).")
    parser.add_argument('--web', action='store_true', help=argparse.SUPPRESS)

    # Additional arguments (passed through)
    parser.add_argument('--engine-debug', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--propagate-evidence', action='store_true',
                        dest='propagate_evidence',
                        default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    parser.add_argument('--propagate-weights', action='store_true', default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('--convergence', '-c', type=float, default=argparse.SUPPRESS,
                        help='stop anytime when bounds are within this range')

    # SDD garbage collection
    sdd_auto_gc_group = parser.add_mutually_exclusive_group()
    sdd_auto_gc_group.add_argument('--sdd-auto-gc', action='store_true', dest='sdd_auto_gc',
                                   default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    sdd_auto_gc_group.add_argument('--sdd-no-auto-gc', action='store_false', dest='sdd_auto_gc',
                                   default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    sdd_fixvars_group = parser.add_mutually_exclusive_group()
    sdd_fixvars_group.add_argument('--sdd-preset-variables', action='store_true',
                                   dest='sdd_preset_variables',
                                   default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    sdd_fixvars_group.add_argument('--sdd-no-preset-variables', action='store_false',
                                   dest='sdd_preset_variables',
                                   default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    return parser


def main(argv, result_handler=None):
    parser = argparser()
    args = parser.parse_args(argv)

    if result_handler is None:
        if args.web:
            result_handler = print_result_json
        else:
            result_handler = print_result

    init_logger(args.verbose)

    if args.output is None:
        output = sys.stdout
    else:
        output = open(args.output, 'w')

    if args.timeout:
        start_timer(args.timeout)

    if len(args.filenames) == 0:
        mode = os.fstat(0).st_mode
        if stat.S_ISFIFO(mode) or stat.S_ISREG(mode):
            # stdin is piped or redirected
            args.filenames = ['-']
        else:
            # stdin is terminal
            # No interactive input, exit
            print('ERROR: Expected a file or stream as input.\n', file=sys.stderr)
            parser.print_help()
            sys.exit(1)

    if args.logspace:
        semiring = SemiringLogProbability()
    else:
        semiring = SemiringProbability()

    if args.symbolic:
        args.koption = 'nnf'
        semiring = SemiringSymbolic()

    if args.propagate_weights:
        args.propagate_weights = semiring

    for filename in args.filenames:
        if len(args.filenames) > 1:
            print ('Results for %s:' % filename)
        result = execute(filename, args.koption, semiring, **vars(args))
        retcode = result_handler(result, output)
        if len(args.filenames) == 1:
            sys.exit(retcode)

    if args.output is not None:
        output.close()

    if args.timeout:
        stop_timer()


if __name__ == '__main__':
    main(sys.argv[1:])
