#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from invoke import run, task, Collection

@task
def clean(docs=False, bytecode=False, extra=''):
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        run("rm -rf %s" % pattern)

@task(default=True)
def build(docs=False):
    run("python setup.py build")
    if docs:
        run("sphinx-build docs docs/_build")

# t=Collection(clean, build)

@task
def worker(good=False):
    '''
    good
    '''
    run("python labkit/scheduler/worker.py")
    # print "this is task1"

@task
def server():
    # print 'this is task2'
    run("python labkit/scheduler/server.py")


@task
def deploy():
    # print 'this is task2'
    run("cd deploy; ansible-playbook deploy.yml")

@task
def rollback():
    # print 'this is task2'
    run("cd deploy; ansible-playbook rollback.yml")

# ns = Collection(test, t=t)
