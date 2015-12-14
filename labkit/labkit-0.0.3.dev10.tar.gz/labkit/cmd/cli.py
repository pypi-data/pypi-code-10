#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# from general import gs
# import labkit.init_gs

# import sys
# sys.argv[1:]=[]
#

#
# @register
# def push_to(queue_names='tasks',yml_file='task.yml'):
#     '''
#     push a task to a specific queue
#
#     :param queue_names:
#     :return:
#     '''
#     # push
#     import sys
#     from labkit.scheduler.push_task_file import push_file
#     # queue_names=queue_names.split()
#     sys.exit(push_file(queue_names))

'''
the command line interface for labkit

'''


import sys

from general.cli import (
    kwoargs,autokwoargs,wrapper_decorator,
    register_maker,run,subprocess_shell,subprocess_run
)
import os

register,_functions=register_maker()

# redis_dir='/usr/local/var/db/redis'

beanstalk_dir='/usr/local/var/binlog'


@register
def push(yml_file='task.yml'):
    '''
    push a task to the tasks queue

    :param queue_names:
    :return:
    '''
    # push
    from labkit.scheduler.push import push_task_file
    yml_file=os.path.abspath(yml_file)
    sys.exit(push_task_file(yml_file))

@register
def kick():
    '''
    push a task to the tasks queue

    :param queue_names:
    :return:
    '''
    import beanstalkc
    import labkit.init_gs
    from general import gs
    bq = beanstalkc.Connection(host=gs.CONF.beanstalk_server, port=gs.CONF.beanstalk_port)
    bq.use('tasks')
    # 数量控制
    sys.exit(bq.kick(1))



# @register
# @autokwoargs
# def runner(yml_file='task.yml'):
#     '''
#     run a task locally
#
#     :param queue_names:
#     :return:
#     '''
#     import labkit.init_gs
#
#     from general.interpreter.runner import load_module, eval_conf, run_file
#     run_file(yml_file)


@register
@autokwoargs
def worker(queue_names='compute'):
    '''
    start a worker to do the compute

    :param queue_names:
    :return:
    '''
    # init_gs只需要import一次, 其他地方import gs的时候就是引用的init过的gs, import可以重复多次, 不会重复执行
    import labkit.init_gs

    from labkit.scheduler.worker import start_worker
    queue_names=queue_names.split()
    sys.exit(start_worker(queue_names))

@register
@autokwoargs
def front(queue_names='tasks'):
    '''
    start the server to deal with task

    :param queue_names:
    :return:
    '''
    import labkit.init_gs
    from labkit.scheduler.worker import start_worker
    queue_names=queue_names.split()
    sys.exit(start_worker(queue_names))


@register
def rest():
    '''
    start the rest api server

    :return:
    '''
    # push
    import labkit.init_gs

    from labkit.api.rest import app
    app.run(debug=True)


@register
def start():
    '''
    ensure all service are running, start rest and server

    :return:
    '''
    subprocess_run("honcho start rest server")
    pass


@register
def startdb():
    '''
    start mongodb and redis-server

    :return:
    '''
    subprocess_run("honcho start mongod redis")
    # todo: start mongodb and redis
    pass

# def backup_redis(redis_dir):
#     # todo: redis backup
#     # redis 只需要拷贝appendonly.aof dump.rdb就行了, 位置查看redis.conf的dir项目
#     # 在redis.conf里面配置appendonly yes 开启aof
#     # redis-cli  -h 127.0.0.1  -p  6379  bgrewriteaof 这条作废
#     # todo: 关于立即save, 待验证
#     subprocess_run("redis-cli config set appendonly yes")
#     # subprocess_run('redis-cli config set save ""')
#     subprocess_run('redis-cli save ')
#     subprocess_run('cp -r '+redis_dir+' backup/')
#
# def restore_redis(redis_dir):
#     # todo: redis resotre
#     subprocess_run('cp  backup/redis/appendonly.aof '+redis_dir)
#     subprocess_run('cp  backup/redis/dump.rdb '+redis_dir)

def backup_beanstalk(beanstalk_dir):
    subprocess_run('cp -r '+beanstalk_dir+' backup/')

def restore_beanstalk(beanstalk_dir):
    command='cp -rf backup/binlog '+os.path.dirname(beanstalk_dir)
    print command
    subprocess_shell(command)

def backup_mongo():
    subprocess_run("mongodump -h localhost -d databank -o backup")

def restore_mongo():
    subprocess_run("mongorestore -h localhost -d databank2 --dir=backup/databank")


@register
def backup():
    '''
    backup all data to backup folder

    :return:
    '''
    backup_mongo()
    # backup_redis(redis_dir)
    backup_beanstalk(beanstalk_dir)
    pass



@register
def restore():
    '''
    restore all data from backup folder

    :return:
    '''
    restore_mongo()
    # restore_redis(redis_dir)
    restore_beanstalk(beanstalk_dir)



def cli():
    # alternative分派, 默认分派是函数名, 用字典可以修改默认分派名, 用@kwoargs可以对关键字参数进行分派
    # run(hello_world,alt={"vvv":version, "no_capitalized":hello_world})

    # 分派必须显示说明, 可以传入列表
    description="""
    labkit cli interface
    """
    commands=_functions
    run(commands,description=description)


if __name__ == '__main__':
    cli()




