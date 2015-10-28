"""
problog.engine_stack - Stack-based implementation of grounding engine
---------------------------------------------------------------------

Default implementation of the ProbLog grounding engine.

..
    Part of the ProbLog distribution.

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

import sys

from .logic import Term, ArithmeticError, is_ground
from .engine import UnifyError, instantiate, UnknownClause, UnknownClauseInternal, is_variable
from .engine import NonGroundProbabilisticClause
from .errors import GroundingError
from .engine import ClauseDBEngine, substitute_head_args, substitute_call_args, unify_call_head, \
    unify_call_return
from .engine_builtin import add_standard_builtins, IndirectCallCycleError


class NegativeCycle(GroundingError):
    """The engine does not support negative cycles."""

    def __init__(self, location=None):
        GroundingError.__init__(self, 'Negative cycle detected', location)


class InvalidEngineState(Exception):
    pass


NODE_TRUE = 0
NODE_FALSE = None


def call(obj, args, kwdargs):
    return 'e', obj, args, kwdargs


def new_result(obj, result, ground_node, source, is_last):
    return 'r', obj, (result, ground_node, source, is_last), {}


def complete(obj, source):
    return 'c', obj, (source,), {}


def results_to_actions(resultlist, engine, node, context, target, parent, identifier,
                        transform, is_root, database, **kwdargs):
    """Translates a list of results to actions.

    :param results:
    :param node:
    :param context:
    :param target:
    :param parent:
    :param identifier:
    :param transform:
    :param is_root:
    :param database:
    :param kwdargs:
    :return:
    """

    # Output
    actions = []

    n = len(resultlist)
    if n > 0:
        # Transform all the results to result messages.
        for result, target_node in resultlist:
            n -= 1
            if not is_root:
                target_node = engine.propagate_evidence(database, target,
                                                        node.functor, result, target_node)
            if target_node != NODE_FALSE:
                if transform:
                    result = transform(result)
                if result is None:
                    if n == 0:
                        actions += [complete(parent, identifier)]
                else:
                    if target_node == NODE_TRUE and target.flag('keep_all') \
                            and not node.functor.startswith('_problog'):
                        name = Term(node.functor, *result)
                        target_node = target.add_atom(name, None, None, name=name, source=None)

                    actions += [new_result(parent, result, target_node, identifier, n == 0)]
            elif n == 0:
                actions += [complete(parent, identifier)]
    else:
        # The goal does not have results: send the completion message.
        actions += [complete(parent, identifier)]
    return actions


class StackBasedEngine(ClauseDBEngine):
    def __init__(self, label_all=False, **kwdargs):
        ClauseDBEngine.__init__(self, **kwdargs)

        self.node_types = {}
        self.node_types['fact'] = self.eval_fact
        self.node_types['conj'] = self.eval_conj
        self.node_types['disj'] = self.eval_disj
        self.node_types['neg'] = self.eval_neg
        self.node_types['define'] = self.eval_define
        self.node_types['call'] = self.eval_call
        self.node_types['clause'] = self.eval_clause
        self.node_types['choice'] = self.eval_choice
        self.node_types['builtin'] = self.eval_builtin
        self.node_types['extern'] = self.eval_extern

        self.cycle_root = None
        self.pointer = 0
        self.stack_size = 128
        self.stack = [None] * self.stack_size

        self.stats = [0] * 10

        self.debug = False
        self.trace = False

        self.label_all = label_all

        self.debugger = kwdargs.get('debugger')

    def eval(self, node_id, **kwdargs):
        # print (kwdargs.get('parent'))
        database = kwdargs['database']
        if node_id < 0:
            node_type = 'builtin'
            node = self.get_builtin(node_id)
        else:
            node = database.get_node(node_id)
            node_type = type(node).__name__
        exec_func = self.create_node_type(node_type)
        if exec_func is None:
            if self.unknown == self.UNKNOWN_FAIL:
                return [complete(kwdargs['parent'], kwdargs.get('identifier'))]
            else:
                raise UnknownClauseInternal()
        return exec_func(node_id=node_id, node=node, **kwdargs)

    def create_node_type(self, node_type):
        return self.node_types.get(node_type)

    def load_builtins(self):
        addBuiltIns(self)

    def add_simple_builtin(self, predicate, arity, function):
        return self.add_builtin(predicate, arity, SimpleBuiltIn(function))

    def grow_stack(self):
        self.stack += [None] * self.stack_size
        self.stack_size *= 2

    def shrink_stack(self):
        self.stack_size = 128
        self.stack = [None] * self.stack_size

    def add_record(self, record):
        if self.pointer >= self.stack_size:
            self.grow_stack()
        self.stack[self.pointer] = record
        self.pointer += 1

    def notifyCycle(self, childnode):
        # Optimization: we can usually stop when we reach a node on_cycle.
        #   However, when we swap the cycle root we need to also notify the old cycle root
        #    up to the new cycle root.
        assert self.cycle_root is not None
        root = self.cycle_root.pointer
        # childnode = self.stack[child]
        current = childnode.parent
        actions = []
        while current != root:
            if current is None:
                raise IndirectCallCycleError(
                    location=childnode.database.lineno(childnode.node.location))
            exec_node = self.stack[current]
            if exec_node.on_cycle:
                break
            new_actions = exec_node.createCycle()
            actions += new_actions
            current = exec_node.parent
        return actions

    def checkCycle(self, child, parent):
        current = child
        while current > parent:
            exec_node = self.stack[current]
            if exec_node.on_cycle:
                break
            if isinstance(exec_node, EvalNot):
                raise NegativeCycle(location=exec_node.database.lineno(exec_node.node.location))
            current = exec_node.parent

    def execute(self, node_id, target=None, database=None, subcall=False, is_root=False, **kwdargs):
        """
        Execute the given node.
        :param node_id: pointer of the node in the database
        :param subcall: indicates whether this is a toplevel call or a subcall
        :param target: target datastructure for storing the ground program
        :param database: database containing the logic program to ground
        :param kwdargs: additional arguments
        :return: results of the execution
        """
        # Find out debugging mode.
        self.trace = kwdargs.get('trace')
        self.debug = kwdargs.get('debug') or self.trace
        debugger = self.debugger

        # Initialize the cache/table.
        # This is stored in the target ground program because
        # node ids are only valid in that context.
        if not hasattr(target, '_cache'):
            target._cache = DefineCache()

        # Retrieve the list of actions needed to evaluate the top-level node.
        # parent = kwdargs.get('parent')
        # kwdargs['parent'] = parent

        actions = self.eval(node_id, parent=None, database=database, target=target,
                            is_root=is_root, **kwdargs)

        # Initialize the action stack.
        actions = list(reversed(actions))
        solutions = []

        # Main loop: process actions until there are no more.
        while actions:
            # Pop the next action.
            # An action consists of 4 parts:
            #   - act: the type of action (r, c, e)
            #   - obj: the pointer on which to call the action
            #   - args: the arguments of the action
            #   - context: the execution context
            act, obj, args, context = actions.pop(-1)

            # Inform the debugger.
            if debugger:
                debugger.process_message(act, obj, args, context)

            if obj is None:
                # We have reached the top-level.
                if act == 'r':
                    # A new result is available
                    solutions.append((args[0], args[1]))
                    if args[3]:
                        # Last result received
                        if not subcall and self.pointer != 0:  # pragma: no cover
                            # ERROR: the engine stack should be empty.
                            self.printStack()
                            raise InvalidEngineState('Stack not empty at end of execution!')
                        if not subcall:
                            # Clean up the stack to save memory.
                            self.shrink_stack()
                        return solutions
                elif act == 'c':
                    # Indicates completion of the execution.
                    return solutions
                else:
                    # ERROR: unknown message
                    raise InvalidEngineState('Unknown message!')
            else:
                # We are not at the top-level.
                if act == 'e':
                    # Never clean up in this case because 'obj' doesn't contain a pointer.
                    cleanup = False
                    # We need to execute another node.
                    if self.cycle_root is not None and context['parent'] < self.cycle_root.pointer:
                        # There is an active cycle and we are about to execute a node
                        # outside that cycle.
                        # We first need to close the cycle.
                        next_actions = self.cycle_root.closeCycle(True) + [
                            (act, obj, args, context)]
                    else:
                        try:
                            # Evaluate the next node.
                            next_actions = self.eval(obj, **context)
                            obj = self.pointer
                        except UnknownClauseInternal:
                            # An unknown clause was encountered.
                            # TODO why is this handled here?
                            call_origin = context.get('call_origin')
                            if call_origin is None:
                                sig = 'unknown'
                                raise UnknownClause(sig, location=None)
                            else:
                                loc = database.lineno(call_origin[1])
                                raise UnknownClause(call_origin[0], location=loc)
                else:
                    # The message is 'r' or 'c'. This means 'obj' should be a valid pointer.
                    try:
                        # Retrieve the execution node from the stack.
                        exec_node = self.stack[obj]
                    except IndexError:  # pragma: no cover
                        self.printStack()
                        raise InvalidEngineState('Non-existing pointer: %s' % obj)
                    if exec_node is None:  # pragma: no cover
                        print(act, obj)
                        raise InvalidEngineState('Invalid node at given pointer: %s' % obj)

                    if act == 'r':
                        # A new result was received.
                        cleanup, next_actions = exec_node.new_result(*args, **context)
                    elif act == 'c':
                        # A completion message was received.
                        cleanup, next_actions = exec_node.complete(*args, **context)
                    else:  # pragma: no cover
                        raise InvalidEngineState('Unknown message')

                if not actions and not next_actions and self.cycle_root is not None:
                    # If there are no more actions and we have an active cycle, we should close the cycle.
                    next_actions = self.cycle_root.closeCycle(True)
                # Update the list of actions.
                actions += list(reversed(next_actions))

                # Do debugging.
                if self.debug:  # pragma: no cover
                    self.printStack(obj)
                    if act in 'rco':
                        print(obj, act, args)
                    print([(a, o, x) for a, o, x, t in actions[-10:]])
                    if self.trace:
                        a = sys.stdin.readline()
                        if a.strip() == 'gp':
                            print(target)
                        elif a.strip() == 'l':
                            self.trace = False
                            self.debug = False
                if cleanup:
                    self.cleanup(obj)

        # This should never happen.
        self.printStack()  # pragma: no cover
        print('Collected results:', solutions)  # pragma: no cover
        raise InvalidEngineState('Engine did not complete correctly!')  # pragma: no cover

    def cleanup(self, obj):
        """
        Remove the given node from the stack and lower the pointer.
        :param obj: pointer of the object to remove
        :type obj: int
        """
        if self.cycle_root and self.cycle_root.pointer == obj:
            self.cycle_root = None
        self.stack[obj] = None
        while self.pointer > 0 and self.stack[self.pointer - 1] is None:
            self.pointer -= 1

    def call(self, query, database, target, transform=None, parent=None, **kwdargs):
        node_id = database.find(query)
        if node_id is None:
            node_id = database.get_builtin(query.signature)
            if node_id is None:
                raise UnknownClause(query.signature, database.lineno(query.location))

        return self.execute(node_id, database=database, target=target,
                            context=self.create_context(query.args), **kwdargs)

    def call_intern(self, query, **kwdargs):
        database = kwdargs.get('database')
        node_id = database.find(query)
        if node_id is None:
            node_id = database.get_builtin(query.signature)
            if node_id is None:
                raise UnknownClause(query.signature, database.lineno(query.location))

        call_args = range(0, len(query.args))
        call_term = query.with_args(*call_args)
        call_term.defnode = node_id

        return self.eval_call(None, call_term,
                              context=self.create_context(query.args), **kwdargs)

    def printStack(self, pointer=None):  # pragma: no cover
        print('===========================')
        for i, x in enumerate(self.stack):
            if (pointer is None or pointer - 20 < i < pointer + 20) and x is not None:
                if i == pointer:
                    print('>>> %s: %s' % (i, x))
                elif self.cycle_root is not None and i == self.cycle_root.pointer:
                    print('ccc %s: %s' % (i, x))
                else:
                    print('    %s: %s' % (i, x))

    def eval_fact(self, parent, node_id, node, context, target, identifier, **kwdargs):
        try:
            # Verify that fact arguments unify with call arguments.
            unify_call_head(context, node.args, context)

            if self.label_all:
                name = Term(node.functor, *node.args)
            else:
                name = None
            # Successful unification: notify parent callback.
            target_node = target.add_atom(node_id, node.probability, name=name)
            if target_node is not None:
                return [new_result(parent, self.create_context(node.args), target_node, identifier,
                                  True)]
            else:
                return [complete(parent, identifier)]
        except UnifyError:
            # Failed unification: don't send result.
            # Send complete message.
            return [complete(parent, identifier)]

    def propagate_evidence(self, db, target, functor, args, resultnode):
        if hasattr(target, 'lookup_evidence'):
            return target.lookup_evidence.get(resultnode, resultnode)
        else:
            return resultnode

    def eval_define(self, node, context, target, parent, identifier=None, transform=None,
                    is_root=False, **kwdargs):

        # This function evaluates the 'define' nodes in the database.
        # This is basically the same as evaluating a goal in Prolog.
        # There are three possible situations:
        #   - the goal has been evaluated before (it is in cache)
        #   - the goal is currently being evaluated (i.e. we have a cycle)
        #        we make a distinction between ground goals and non-ground goals
        #   - we have not seen this goal before

        # Extract a descriptor for the current goal being evaluated.
        functor = node.functor
        goal = (functor, context)

        # Look up the results in the cache.
        results = target._cache.get(goal)
        if results is not None:
            # We have results for this goal, i.e. it has been fully evaluated before.
            # Transform the results to actions and return.
            return results_to_actions(results, self, node, context, target, parent, identifier, transform, is_root, **kwdargs)
        else:
            # Look up the results in the currently active nodes.
            active_node = target._cache.getEvalNode(goal)
            if active_node is not None:
                # There is an active node.
                if active_node.is_ground and active_node.results:
                    # If the node is ground, we can simply return the current result node.
                    active_node.flushBuffer(True)
                    active_node.is_cycle_parent = True  # Notify it that it's buffer was flushed
                    queue = results_to_actions(active_node.results, self, node, context, target, parent, identifier, transform, is_root, **kwdargs)
                    assert (len(queue) == 1)
                    self.checkCycle(parent, active_node.pointer)
                    return queue
                else:
                    # If the node in non-ground, we need to create an evaluation node.
                    evalnode = EvalDefine(pointer=self.pointer, engine=self, node=node,
                                          context=context, target=target, identifier=identifier,
                                          parent=parent, transform=transform, is_root=is_root,
                                          **kwdargs)
                    self.add_record(evalnode)
                    return evalnode.cycleDetected(active_node)
            else:
                # The node has not been seen before.
                # Get the children that may fit the context (can contain false positives).
                children = node.children.find(context)
                to_complete = len(children)

                if to_complete == 0:
                    # No children, so complete immediately.
                    return [complete(parent, identifier)]
                else:
                    # Children to evaluate, so start evaluation node.
                    evalnode = EvalDefine(to_complete=to_complete, pointer=self.pointer,
                                          engine=self, node=node, context=context, target=target,
                                          identifier=identifier, transform=transform, parent=parent,
                                          **kwdargs)
                    self.add_record(evalnode)
                    target._cache.activate(goal, evalnode)
                    actions = [evalnode.createCall(child) for child in children]
                    return actions

    def eval_conj(self, **kwdargs):
        return self.eval_default(EvalAnd, **kwdargs)

    def eval_disj(self, parent, node, **kwdargs):
        if len(node.children) == 0:
            # No children, so complete immediately.
            return [complete(parent, None)]
        else:
            evalnode = EvalOr(pointer=self.pointer, engine=self, parent=parent, node=node,
                              **kwdargs)
            self.add_record(evalnode)
            return [evalnode.createCall(child) for child in node.children]

    def eval_neg(self, **kwdargs):
        return self.eval_default(EvalNot, **kwdargs)

    def eval_call(self, node_id, node, context, parent, transform=None, identifier=None, **kwdargs):
        call_args, var_translate = substitute_call_args(node.args, context)
        min_var = self._context_min_var(context)

        if self.debugger:
            self.debugger.call_create(node_id, node.functor, call_args, parent)

        ground_mask = [not is_ground(c) for c in call_args]

        def result_transform(result):
            output = self._clone_context(context)
            try:
                assert (len(result) == len(node.args))
                output = unify_call_return(result, node.args, output, var_translate, min_var,
                                           mask=ground_mask)
                if self.debugger:
                    self.debugger.call_result(node_id, node.functor, call_args, result)
                return output
            except UnifyError:
                pass

        if transform is None:
            transform = Transformations()

        transform.addFunction(result_transform)

        origin = '%s/%s' % (node.functor, len(node.args))
        kwdargs['call_origin'] = (origin, node.location)
        kwdargs['context'] = self.create_context(call_args)
        kwdargs['transform'] = transform

        try:
            return self.eval(node.defnode, parent=parent, identifier=identifier, **kwdargs)
        except UnknownClauseInternal:
            loc = kwdargs['database'].lineno(node.location)
            raise UnknownClause(origin, location=loc)

    def _context_min_var(self, context):
        min_var = 0
        for c in context:
            if is_variable(c):
                if c is not None and c < 0:
                    min_var = min(min_var, c)
            else:
                variables = [v for v in c.variables() if v is not None]
                if variables:
                    min_var = min(min_var, min(variables))
        return min_var

    def eval_clause(self, context, node, node_id, parent, transform=None, identifier=None,
                    **kwdargs):
        new_context = self.create_context([None] * node.varcount)

        try:
            unify_call_head(context, node.args, new_context)
            # Note: new_context should not contain None values.
            # We should replace these with negative numbers.
            # 1. Find lowest negative number in new_context.
            #   TODO better option is to store this in context somewhere
            min_var = self._context_min_var(new_context)
            # 2. Replace None in new_context with negative values
            cc = min_var
            for i, c in enumerate(new_context):
                if c is None:
                    cc -= 1
                    new_context[i] = cc
            if transform is None:
                transform = Transformations()

            def result_transform(result):
                output = substitute_head_args(node.args, result)
                return self.create_context(output)

            transform.addFunction(result_transform)
            return self.eval(node.child, context=new_context, parent=parent, transform=transform,
                             **kwdargs)
        except UnifyError:
            # Call and clause head are not unifiable, just fail (complete without results).
            return [complete(parent, identifier)]

    def handle_nonground(self, location=None, database=None, node=None, **kwdargs):
        raise NonGroundProbabilisticClause(location=database.lineno(node.location))

    def eval_choice(self, parent, node_id, node, context, target, database, identifier, **kwdargs):
        result = self._fix_context(context)

        for i, r in enumerate(result):
            if i not in node.locvars and not is_ground(r):
                result = self.handle_nonground(result=result, node=node, target=target,
                                               database=database,
                                               context=context, parent=parent, node_id=node_id,
                                               identifier=identifier, **kwdargs)

        probability = instantiate(node.probability, result)
        # Create a new atom in ground program.

        if self.label_all:
            name = Term(node.functor, *result)
        else:
            name = None

        origin = (node.group, result)
        ground_node = target.add_atom(origin + (node.choice,), probability, group=origin, name=name)
        # Notify parent.

        if ground_node is not None:
            return [new_result(parent, result, ground_node, identifier, True)]
        else:
            return [complete(parent, identifier)]

    def eval_extern(self, node=None, **kwdargs):
        return self.eval_builtin(node=SimpleBuiltIn(node.function), **kwdargs)

    def eval_builtin(self, **kwdargs):
        return self.eval_default(EvalBuiltIn, **kwdargs)

    def eval_default(self, eval_type, **kwdargs):
        node = eval_type(pointer=self.pointer, engine=self, **kwdargs)
        cleanup, actions = node()  # Evaluate the node
        if not cleanup:
            self.add_record(node)
        return actions


class EvalNode(object):
    def __init__(self, engine, database, target, node_id, node, context, parent, pointer,
                 identifier=None, transform=None, call=None, **extra):
        self.engine = engine
        self.database = database
        self.target = target
        self.node_id = node_id
        self.node = node
        self.context = context
        self.parent = parent
        self.identifier = identifier
        self.pointer = pointer
        self.transform = transform
        self.call = call
        self.on_cycle = False

    def notifyResult(self, arguments, node=0, is_last=False, parent=None):
        if parent is None:
            parent = self.parent
        if self.transform:
            arguments = self.transform(arguments)
        if arguments is None:
            if is_last:
                return self.notifyComplete()
            else:
                return []
        else:
            return [new_result(parent, arguments, node, self.identifier, is_last)]

    def notifyComplete(self, parent=None):
        if parent is None:
            parent = self.parent
        return [complete(parent, self.identifier)]

    def createCall(self, node_id, *args, **kwdargs):
        base_args = {}
        base_args['database'] = self.database
        base_args['target'] = self.target
        base_args['context'] = self.context
        base_args['parent'] = self.pointer
        base_args['identifier'] = self.identifier
        base_args['transform'] = None
        base_args['call'] = self.call
        base_args.update(kwdargs)
        return call(node_id, args, base_args)

    def createCycle(self):
        self.on_cycle = True
        return []

    def node_str(self):  # pragma: no cover
        return str(self.node)

    def __str__(self):  # pragma: no cover
        if hasattr(self.node, 'location'):
            pos = self.database.lineno(self.node.location)
        else:
            pos = None
        if pos is None:
            pos = '??'
        node_type = self.__class__.__name__[4:]
        return '%s %s %s [at %s:%s] | Context: %s' % (
            self.parent, node_type, self.node_str(), pos[0], pos[1], self.context) + ' {' + str(
            self.transform) + '}'


class EvalOr(EvalNode):
    # Has exactly one listener (parent)
    # Has C children.
    # Behaviour:
    # - 'call' creates child nodes and request calls to them
    # - 'call' calls complete if there are no children (C = 0)
    # - 'new_result' is forwarded to parent
    # - 'complete' waits until it is called C times, then sends signal to parent
    # Can be cleanup after 'complete' was sent

    def __init__(self, **parent_args):
        EvalNode.__init__(self, **parent_args)
        self.results = ResultSet()
        self.to_complete = len(self.node.children)
        self.engine.stats[0] += 1

    def isOnCycle(self):
        return self.on_cycle

    def flushBuffer(self, cycle=False):
        func = lambda result, nodes: self.target.add_or(nodes, readonly=(not cycle), name=None)
        self.results.collapse(func)

    def new_result(self, result, node=NODE_TRUE, source=None, is_last=False):
        if self.isOnCycle():
            res = self.engine._fix_context(result)
            assert self.results.collapsed
            if res in self.results:
                res_node = self.results[res]
                self.target.add_disjunct(res_node, node)
                return False, []
            else:
                result_node = self.target.add_or((node,), readonly=False, name=None)
                self.results[res] = result_node
                actions = []
                if self.isOnCycle():
                    actions += self.notifyResult(res, result_node)
                if is_last:
                    a, act = self.complete(source)
                    actions += act
                else:
                    a = False
                return a, actions
        else:
            assert (not self.results.collapsed)
            res = self.engine._fix_context(result)
            self.results[res] = node
            if is_last:
                return self.complete(source)
            else:
                return False, []

    def complete(self, source=None):
        self.to_complete -= 1
        if self.to_complete == 0:
            self.flushBuffer()
            actions = []
            if not self.isOnCycle():
                for result, node in self.results:
                    actions += self.notifyResult(result, node)
            actions += self.notifyComplete()
            return True, actions
        else:
            return False, []

    def createCycle(self):
        self.on_cycle = True
        self.flushBuffer(True)
        actions = []
        for result, node in self.results:
            actions += self.notifyResult(result, node)
        return actions

    def node_str(self):  # pragma: no cover
        return ''

    def __str__(self):  # pragma: no cover
        return EvalNode.__str__(self) + ' tc: ' + str(self.to_complete)


class NestedDict(object):
    def __init__(self):
        self.__base = {}

    def __getitem__(self, key):
        p_key, s_key = key
        p_key = (p_key, len(s_key))
        elem = self.__base[p_key]
        for s in s_key:
            elem = elem[s]
        return elem

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        p_key, s_key = key
        p_key = (p_key, len(s_key))
        try:
            elem = self.__base[p_key]
            for s in s_key:
                elem = elem[s]
            return True
        except KeyError:
            return False

    def __setitem__(self, key, value):
        p_key, s_key = key
        p_key = (p_key, len(s_key))
        if s_key:
            elem = self.__base.get(p_key)
            if elem is None:
                elem = {}
                self.__base[p_key] = elem
            for s in s_key[:-1]:
                elemN = elem.get(s)
                if elemN is None:
                    elemN = {}
                    elem[s] = elemN
                elem = elemN
            elem[s_key[-1]] = value
        else:
            self.__base[p_key] = value

    def __delitem__(self, key):
        p_key, s_key = key
        p_key = (p_key, len(s_key))
        if s_key:
            elem = self.__base[p_key]
            elems = [(p_key, self.__base, elem)]
            for s in s_key[:-1]:
                elem_n = elem[s]
                elems.append((s, elem, elem_n))
                elem = elem_n
            del elem[s_key[-1]]  # Remove last element
            for s, e, ec in reversed(elems):
                if len(ec) == 0:
                    del e[s]
                else:
                    break
        else:
            del self.__base[p_key]

    def __str__(self):  # pragma: no cover
        return str(self.__base)


class DefineCache(object):
    def __init__(self):
        self.__non_ground = NestedDict()
        self.__ground = NestedDict()
        self.__active = NestedDict()

    def is_dont_cache(self, goal):
        return goal[0][:9] == '_nocache_'

    def activate(self, goal, node):
        self.__active[goal] = node

    def deactivate(self, goal):
        del self.__active[goal]

    def getEvalNode(self, goal):
        return self.__active.get(goal)

    def __setitem__(self, goal, results):
        if self.is_dont_cache(goal):
            return
        # Results
        functor, args = goal
        if is_ground(*args):
            if results:
                # assert(len(results) == 1)
                res_key = next(iter(results.keys()))
                key = (functor, res_key)
                self.__ground[key] = results[res_key]
            else:
                key = (functor, args)
                self.__ground[key] = NODE_FALSE  # Goal failed
        else:
            res_keys = list(results.keys())
            self.__non_ground[goal] = results
            for res_key in res_keys:
                key = (functor, res_key)
                self.__ground[key] = results[res_key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, goal):
        functor, args = goal
        if is_ground(*args):
            return [(args, self.__ground[goal])]
        else:
            # res_keys = self.__non_ground[goal]
            return self.__non_ground[goal].items()

    def __contains__(self, goal):
        functor, args = goal
        if is_ground(*args):
            return goal in self.__ground
        else:
            return goal in self.__non_ground

    def __str__(self):  # pragma: no cover
        return '%s\n%s' % (self.__non_ground, self.__ground)


class ResultSet(object):
    def __init__(self):
        self.results = []
        self.index = {}
        self.collapsed = False

    def __setitem__(self, result, node):
        index = self.index.get(result)
        if index is None:
            index = len(self.results)
            self.index[result] = index
            if self.collapsed:
                self.results.append((result, node))
            else:
                self.results.append((result, [node]))
        else:
            assert (not self.collapsed)
            self.results[index][1].append(node)

    def __getitem__(self, result):
        index = self.index[result]
        result, node = self.results[index]
        return node

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return None

    def keys(self):
        return [result for result, node in self.results]

    def items(self):
        return self.results

    def __len__(self):
        return len(self.results)

    def collapse(self, function):
        if not self.collapsed:
            for i, v in enumerate(self.results):
                result, node = v
                collapsed_node = function(result, node)
                self.results[i] = (result, collapsed_node)
            self.collapsed = True

    def __contains__(self, key):
        return key in self.index

    def __iter__(self):
        return iter(self.results)

    def __str__(self):  # pragma: no cover
        return str(self.results)


class EvalDefine(EvalNode):
    # A buffered Define node.
    def __init__(self, call=None, to_complete=None, is_root=False, **parent_args):
        EvalNode.__init__(self, **parent_args)
        # self.__buffer = defaultdict(list)
        # self.results = None

        self.results = ResultSet()

        self.cycle_children = []
        self.cycle_close = set()
        self.is_cycle_root = False
        self.is_cycle_child = False
        self.is_cycle_parent = False

        self.call = (self.node.functor, self.context)
        self.to_complete = to_complete
        self.is_ground = is_ground(*self.context)
        self.is_root = is_root
        self.engine.stats[1] += 1

    def notifyResult(self, arguments, node=0, is_last=False, parent=None):
        if not self.is_root:
            node = self.engine.propagate_evidence(self.database, self.target, self.node.functor,
                                                  arguments, node)
        return super(EvalDefine, self).notifyResult(arguments, node, is_last, parent)

    def notifyResultMe(self, arguments, node=0, is_last=False):
        parent = self.pointer
        return [new_result(parent, arguments, node, self.identifier, is_last)]

    def notifyResultChildren(self, arguments, node=0, is_last=False):
        parents = self.cycle_children
        return [new_result(parent, arguments, node, self.identifier, is_last) for parent in parents]

    def new_result(self, result, node=NODE_TRUE, source=None, is_last=False):
        if self.is_cycle_child:
            if is_last:
                return True, self.notifyResult(result, node, is_last=is_last)
            else:
                return False, self.notifyResult(result, node, is_last=is_last)
        else:
            if self.isOnCycle() or self.isCycleParent():
                assert self.results.collapsed
                res = self.engine._fix_context(result)
                res_node = self.results.get(res)
                if res_node is not None:
                    self.target.add_disjunct(res_node, node)
                    actions = []
                    if is_last:
                        a, act = self.complete(source)
                        actions += act
                    else:
                        a = False
                    return a, actions
                else:
                    cache_key = (self.node.functor, res)
                    if cache_key in self.target._cache:
                        # Get direct
                        stored_result = self.target._cache[cache_key]
                        assert (len(stored_result) == 1)
                        result_node = stored_result[0][1]

                        if not self.is_root:
                            result_node = self.engine.propagate_evidence(self.database, self.target, self.node.functor, res, result_node)
                    else:
                        if self.engine.label_all:
                            name = Term(self.node.functor, *res)
                        else:
                            name = None
                            if not self.is_root:
                                node = self.engine.propagate_evidence(self.database, self.target, self.node.functor, res, node)
                        result_node = self.target.add_or((node,), readonly=False, name=name)
                    # if self.engine.label_all :
                    #     name = str(Term(self.node.functor, *res))
                    #     self.target.addName(name, result_node, self.target.LABEL_NAMED)
                    self.results[res] = result_node
                    actions = []
                    # Send results to cycle children
                    # actions += self.notifyResultChildren(res, result_node)
                    # if self.pointer == 49336 :
                    #     self.engine.debug = True
                    #     self.engine.trace = True
                    if self.isOnCycle() and result_node is not NODE_FALSE:
                        actions += self.notifyResult(res, result_node)

                    # TODO what if result_node is NONE?
                    actions += self.notifyResultChildren(res, result_node, is_last=False)
                    # TODO the following optimization doesn't always work, see test/some_cycles.pl
                    # actions += self.notifyResultChildren(res, result_node, is_last=self.is_ground)
                    # if self.is_ground :
                    #     self.engine.cycle_root.cycle_close -= set(self.cycle_children)

                    if is_last:
                        a, act = self.complete(source)
                        actions += act
                    else:
                        a = False
                    return a, actions
            else:
                assert (not self.results.collapsed)
                res = self.engine._fix_context(result)
                self.results[res] = node
                if is_last:
                    return self.complete(source)
                else:
                    return False, []

    def complete(self, source=None):
        if self.is_cycle_child:
            return True, self.notifyComplete()
        else:
            self.to_complete -= 1
            if self.to_complete == 0:
                cache_key = (self.node.functor, self.context)
                # assert (not cache_key in self.target._cache)
                self.flushBuffer()
                self.target._cache[cache_key] = self.results
                self.target._cache.deactivate(cache_key)
                actions = []
                if not self.isOnCycle():
                    actions = results_to_actions(self.results, **vars(self))
                else:
                    actions += self.notifyComplete()
                return True, actions
            else:
                return False, []

    def flushBuffer(self, cycle=False):
        def func(res, nodes):
            cache_key = (self.node.functor, res)
            if cache_key in self.target._cache:
                stored_result = self.target._cache[cache_key]
                assert (len(stored_result) == 1)
                node = stored_result[0][1]
                if not self.is_root:
                    node = self.engine.propagate_evidence(self.database, self.target, self.node.functor, res, node)
            else:
                if self.engine.label_all:
                    name = Term(self.node.functor, *res)
                else:
                    name = None

                if not self.is_root:
                    new_nodes = []
                    for node in nodes:
                        node = self.engine.propagate_evidence(self.database, self.target, self.node.functor, res, node)
                        new_nodes.append(node)
                    nodes = new_nodes
                node = self.target.add_or(nodes, readonly=(not cycle), name=name)
            # node = self.target.add_or( nodes, readonly=(not cycle) )
            # if self.engine.label_all:
            #     name = str(Term(self.node.functor, *res))
            #     self.target.addName(name, node, self.target.LABEL_NAMED)
            return node
        self.results.collapse(func)

    def isOnCycle(self):
        return self.on_cycle

    def isCycleParent(self):
        return bool(self.cycle_children) or self.is_cycle_parent

    def cycleDetected(self, cycle_parent):
        queue = []
        goal = (self.node.functor, self.context)
        # Get the top node of this cycle.
        cycle_root = self.engine.cycle_root
        # Mark this node as a cycle child
        self.is_cycle_child = True
        # Register this node as a cycle child of cycle_parent
        cycle_parent.cycle_children.append(self.pointer)

        cycle_parent.flushBuffer(True)
        for result, node in cycle_parent.results:
            queue += self.notifyResultMe(result, node)

        if cycle_root is not None and cycle_parent.pointer < cycle_root.pointer:
            # New parent is earlier in call stack as current cycle root
            # Unset current root
            # Unmark current cycle root
            cycle_root.is_cycle_root = False
            # Copy subcycle information from old root to new root
            cycle_parent.cycle_close = cycle_root.cycle_close
            cycle_root.cycle_close = set()
            self.engine.cycle_root = cycle_parent
            queue += cycle_root.createCycle()
            queue += self.engine.notifyCycle(
                cycle_root)  # Notify old cycle root up to new cycle root
            cycle_root = None
        if cycle_root is None:  # No active cycle
            # Register cycle root with engine
            self.engine.cycle_root = cycle_parent
            # Mark parent as cycle root
            cycle_parent.is_cycle_root = True
            #
            cycle_parent.cycle_close.add(self.pointer)
            # Queue a create cycle message that will be passed up the call stack.
            queue += self.engine.notifyCycle(self)
            # Send a close cycle message to the cycle root.
        else:  # A cycle is already active
            # The new one is a subcycle
            # if not self.is_ground :
            cycle_root.cycle_close.add(self.pointer)
            # Queue a create cycle message that will be passed up the call stack.
            queue += self.engine.notifyCycle(self)
        return queue

    def closeCycle(self, toplevel):
        if self.is_cycle_root and toplevel:
            self.engine.cycle_root = None
            actions = []
            for cc in self.cycle_close:
                actions += self.notifyComplete(parent=cc)
            return actions
        else:
            return []

    def createCycle(self):
        if self.on_cycle:  # Already on cycle
            # Pass message to parent
            return []
        elif self.is_cycle_root:
            return []
        else:
            # Define node
            self.on_cycle = True
            self.flushBuffer(True)
            actions = []
            for result, node in self.results:
                actions += self.notifyResult(result, node)
            return actions

    def node_str(self):  # pragma: no cover
        return str(Term(self.node.functor, *self.context))

    def __str__(self):  # pragma: no cover
        extra = ['tc: %s' % self.to_complete]
        if self.is_cycle_child:
            extra.append('CC')
        if self.is_cycle_root:
            extra.append('CR')
        if self.isCycleParent():
            extra.append('CP')
        if self.on_cycle:
            extra.append('*')
        if self.cycle_children:
            extra.append('c_ch: %s' % (self.cycle_children,))
        if self.cycle_close:
            extra.append('c_cl: %s' % (self.cycle_close,))
        return EvalNode.__str__(self) + ' ' + ' '.join(extra)


class EvalNot(EvalNode):
    # Has exactly one listener (parent)
    # Has 1 child.
    # Behaviour:
    # - 'new_result' stores results and does not request actions
    # - 'complete: sends out new_results and complete signals
    # Can be cleanup after 'complete' was sent

    def __init__(self, **parent_args):
        EvalNode.__init__(self, **parent_args)
        self.nodes = set()  # Store ground nodes
        self.engine.stats[2] += 1

    def __call__(self):
        return False, [self.createCall(self.node.child)]

    def new_result(self, result, node=NODE_TRUE, source=None, is_last=False):
        if node != NODE_FALSE:
            self.nodes.add(node)
        if is_last:
            return self.complete(source)
        else:
            return False, []

    def complete(self, source=None):
        actions = []
        if self.nodes:
            or_node = self.target.add_not(self.target.add_or(self.nodes, name=None))
            if or_node != NODE_FALSE:
                actions += self.notifyResult(self.context, or_node)
        else:
            if self.target.flag('keep_all'):
                src_node = self.database.get_node(self.node.child)
                args, _ = substitute_call_args(src_node.args, self.context)
                name = Term(src_node.functor, *args)
                node = -self.target.add_atom(name, False, None, name=name, source='negation')
            else:
                node = NODE_TRUE

            actions += self.notifyResult(self.context, node)
        actions += self.notifyComplete()
        return True, actions

    def createCycle(self):
        raise NegativeCycle(location=self.database.lineno(self.node.location))

    def node_str(self):  # pragma: no cover
        return ''


class Transformations(object):
    def __init__(self):
        self.functions = []
        self.constant = None

    def addConstant(self, constant):
        pass
        # if self.constant is None :
        #     self.constant = self(constant)
        #     self.functions = []

    def addFunction(self, function):
        # print ('add', function, self.constant)
        # if self.constant is None :
        self.functions.append(function)

    def __call__(self, result):
        # if self.constant != None :
        #     return self.constant
        # else :
        for f in reversed(self.functions):
            if result is None:
                return None
            result = f(result)
        return result


class EvalAnd(EvalNode):
    def __init__(self, **parent_args):
        EvalNode.__init__(self, **parent_args)
        self.to_complete = 1
        self.engine.stats[3] += 1

    def __call__(self):
        return False, [self.createCall(self.node.children[0], identifier=None)]

    def new_result(self, result, node=0, source=None, is_last=False):
        if source is None:  # Result from the first conjunct.
            # We will create a second conjunct, which needs to send a 'complete' signal.
            self.to_complete += 1
            if is_last:
                # Notify self that this conjunct is complete. ('all_complete' will always be False)
                all_complete, complete_actions = self.complete()
                # if False and node == NODE_TRUE :
                #     # TODO THERE IS A BUG HERE
                #     # If there is only one node to complete (the new second conjunct) then
                #     #  we can clean up this node, but then we would lose the ground node of
                #     #  the first conjunct.
                #     # This is ok when it is deterministically true.  TODO make this always ok!
                #     # We can redirect the second conjunct to our parent.
                #     return (self.to_complete==1),
                # [ self.createCall( self.node.children[1], context=result, parent=self.parent ) ]
                # else :
                return False, [
                    self.createCall(self.node.children[1], context=result, identifier=node)]
            else:
                # Not the last result: default behaviour
                return False, [
                    self.createCall(self.node.children[1], context=result, identifier=node)]
        else:  # Result from the second node
            # Make a ground node
            target_node = self.target.add_and((source, node), name=None)
            if is_last:
                # Notify self of child completion
                all_complete, complete_actions = self.complete()
            else:
                all_complete, complete_actions = False, []
            if all_complete:
                return True, self.notifyResult(result, target_node, is_last=True)
            else:
                return False, self.notifyResult(result, target_node, is_last=False)

    def complete(self, source=None):
        self.to_complete -= 1
        if self.to_complete == 0:
            return True, self.notifyComplete()
        else:
            assert (self.to_complete > 0)
            return False, []

    def node_str(self):  # pragma: no cover
        return ''

    def __str__(self):  # pragma: no cover
        return EvalNode.__str__(self) + ' tc: %s' % self.to_complete


class EvalBuiltIn(EvalNode):
    def __init__(self, call_origin=None, **kwdargs):
        EvalNode.__init__(self, **kwdargs)
        if call_origin is not None:
            self.location = call_origin[1]
        else:
            self.location = None
        self.call_origin = call_origin
        self.engine.stats[4] += 1

    def __call__(self):
        try:
            return self.node(*self.context, engine=self.engine, database=self.database,
                             target=self.target, location=self.location, callback=self,
                             transform=self.transform, parent=self.parent,
                             call_origin=self.call_origin)
        except ArithmeticError as err:
            if self.database and self.location:
                functor = self.call_origin[0].split('/')[0]
                callterm = Term(functor, *self.context)
                err.base_message = 'Error while evaluating %s: %s' % (callterm, err.base_message)
                err.location = self.database.lineno(self.location)
            raise err


class BooleanBuiltIn(object):
    """Simple builtin that consist of a check without unification. \
      (e.g. var(X), integer(X), ... )."""

    def __init__(self, base_function):
        self.base_function = base_function

    def __call__(self, *args, **kwdargs):
        callback = kwdargs.get('callback')
        if self.base_function(*args, **kwdargs):
            args = kwdargs['engine'].create_context(args)
            if kwdargs['target'].flag('keep_builtins'):
                call = kwdargs['call_origin'][0].split('/')[0]
                name = Term(call, *args)
                node = kwdargs['target'].add_atom(name, None, None, name=name, source='builtin')

                return True, callback.notifyResult(args, node, True)
            else:
                return True, callback.notifyResult(args, NODE_TRUE, True)
        else:
            return True, callback.notifyComplete()

    def __str__(self):  # pragma: no cover
        return str(self.base_function)


class SimpleBuiltIn(object):
    """Simple builtin that does cannot be involved in a cycle or require engine information \
    and has 0 or more results."""

    def __init__(self, base_function):
        self.base_function = base_function

    def __call__(self, *args, **kwdargs):
        callback = kwdargs.get('callback')
        results = self.base_function(*args, **kwdargs)
        output = []
        if results:
            for i, result in enumerate(results):
                result = kwdargs['engine'].create_context(result)

                if kwdargs['target'].flag('keep_builtins'):
                    # kwdargs['target'].add_node()
                    # print (kwdargs.keys(), args)
                    call = kwdargs['call_origin'][0].split('/')[0]
                    name = Term(call, *result)
                    node = kwdargs['target'].add_atom(name, None, None, name=name, source='builtin')
                    output += callback.notifyResult(result, node, i == len(results) - 1)
                else:
                    output += callback.notifyResult(result, NODE_TRUE, i == len(results) - 1)
            return True, output
        else:
            return True, callback.notifyComplete()

    def __str__(self):  # pragma: no cover
        return str(self.base_function)


class SimpleProbabilisticBuiltIn(object):
    """Simple builtin that does cannot be involved in a cycle or require engine information and has 0 or more results."""

    def __init__(self, base_function):
        self.base_function = base_function

    def __call__(self, *args, **kwdargs):
        callback = kwdargs.get('callback')
        results = self.base_function(*args, **kwdargs)
        output = []
        if results:
            for i, result in enumerate(results):
                output += callback.notifyResult(kwdargs['engine'].create_context(result[0]),
                                                result[1], i == len(results) - 1)
            return True, output
        else:
            return True, callback.notifyComplete()

    def __str__(self):  # pragma: no cover
        return str(self.base_function)


def addBuiltIns(engine):
    add_standard_builtins(engine, BooleanBuiltIn, SimpleBuiltIn, SimpleProbabilisticBuiltIn)
