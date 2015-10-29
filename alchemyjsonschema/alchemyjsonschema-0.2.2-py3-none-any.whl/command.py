# -*- coding:utf-8 -*-
import inspect
import sys
import pkg_resources
import json
import argparse


from . import (
    SchemaFactory,
    AlsoChildrenWalker,
    OneModelOnlyWalker,
    SingleModelWalker,
    HandControlledWalkerFactory,
    RelationDesicion,
    ComfortableDesicion
)


def import_symbol(symbol):  # todo cache
    return pkg_resources.EntryPoint.parse("x=%s" % symbol).load(False)


def err(x):
    sys.stderr.write(x)
    sys.stderr.write("\n")
    sys.stderr.flush()


def detect_walker(x):
    if x == "structual":
        return AlsoChildrenWalker
    elif x == "noforeignkey":
        return OneModelOnlyWalker
    elif x == "foreignkey":
        return SingleModelWalker
    elif x == "control":
        return HandControlledWalkerFactory
    else:
        raise Exception(x)


def detect_decision(x):
    if x == "default":
        return RelationDesicion()
    elif x == "comfortable":
        return ComfortableDesicion()
    else:
        raise Exception(x)


def write_output_file(schema, model, outdir):
    fname = model.__tablename__ + ".json"
    schemaf = outdir + "/" + fname
    f = open(schemaf, 'w')
    f.write(schema)
    f.close()


def handle_output(schema, model, outdir=None):
    if outdir is None:
        print(schema)
    else:
        write_output_file(schema, model, outdir)


def run(walker, model=None, module=None, depth=None,
        relation_decision=None, outdir=None):
    make_schema = SchemaFactory(walker, relation_decision=relation_decision)

    if model is not None:
        # default behavior
        schema = make_schema(model, depth=depth)
        handle_output(json.dumps(schema, indent=2, ensure_ascii=False),
                      model, outdir=outdir)
    elif module is not None:
        # iterate over attributes of module looking for orm objects
        for name in module.__all__:
            basemodel = getattr(module, name)
            schema = make_schema(basemodel, depth=depth)
            handle_output(json.dumps(schema, indent=2, ensure_ascii=False),
                          basemodel, outdir=outdir)
    else:
        print "Error: Target was neither a model nor a module."


def main(sys_args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help='the module or class to extract schemas from')
    parser.add_argument("--walker", choices=["noforeignkey", "foreignkey", "structual", "control"], default="structual")
    parser.add_argument("--decision", choices=["default", "comfortable"], default="default")
    parser.add_argument("--depth", default=None, type=int)
    parser.add_argument("--decision-relationship", default="")
    parser.add_argument("--decision-foreignkey", default="")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args(sys_args)
    model = None
    module = None
    rawtarget = import_symbol(args.target)
    if inspect.isclass(rawtarget):
        model = rawtarget
    else:
        module = rawtarget
    walker = detect_walker(args.walker)
    if walker == HandControlledWalkerFactory:
        decisions = {k.strip(): "relationship" for k in args.decision_relationship.split(" ")}
        decisions.update({k.strip(): "foreignkey" for k in args.decision_foreignkey.split(" ")})
        walker = walker(decisions)
    return run(walker, model=model,
               module=module, depth=args.depth,
               relation_decision=detect_decision(args.decision),
               outdir=args.out_dir)
