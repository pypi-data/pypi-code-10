#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
from flask import Flask, jsonify

app = Flask(__name__)
# app.config.from_object('config')

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask.ext.stormpath import (
    StormpathError,
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)

from flask.ext.cors import CORS


app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'K7DzZX8LgzpxXC'
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey.properties'
app.config['STORMPATH_APPLICATION'] = 'stock'

stormpath_manager = StormpathManager(app)



# api:
# /api/ensembles(所有ensemble列表)/ensemble_name(ensemble的统计, 前几名)/conformer_name(具体信息)
# /api/tasks(tasks列表)/task_name(具体信息)
# 暂时无post操作.

# import rq_dashboard


app = Flask(__name__)

# app.config.from_object(rq_dashboard.default_settings)
# app.register_blueprint(rq_dashboard.blueprint,url_prefix='/api/rq')

CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

from general.cli import subprocess_run



if __name__ == "__main__":
    app.run()



from flask import make_response
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


import os
@app.route('/api/start_server', methods=['POST'])
def start_server():
    # os.system("/Users/lhr/_env/auto/commands/labkit server")
    return ""


@app.route('/api/start_worker', methods=['POST'])
def start_worker():
    # os.system("/Users/lhr/_env/auto/commands/labkit  worker")
    return ""


@auth.get_password
def get_password(username):
    if username == 'lhr':
        return 'passwd'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# from state.refresh_data import get_set_name_list,get_set_list, get_data,get_all_id_list
# from core.algorithm.stage1 import buy_sell_point_by_id,calc_stage1

@app.route('/stock/api/setlist', methods=['GET'])
# @auth.login_required
def json_get_set_name_list():
    return jsonify({'set_name_list': get_set_name_list()})


@app.route('/stock/api/setlist/<set_name>', methods=['GET'])
def josn_get_set_list(set_name):
    return jsonify({set_name: get_set_list(set_name)})

@app.route('/stock/api/setlist/<set_name>/<listtype>', methods=['GET'])
def json_get_buy_list(set_name,listtype):
    try:
        return jsonify({set_name:{listtype: select_stock.get_buy_list(set_name,listtype)}})
    except:
        abort(404)

@app.route('/stock/api/setlist/<set_name>/<listtype>/<id>', methods=['GET'])
def json_get_data_by_id(set_name,listtype,id):
    '''
    good
    '''
    return jsonify({id: buy_sell_point_by_id(id).to_json()})

@app.route('/stock/api/<id>', methods=['GET'])
def json_get_data_by_id2(id):
    return jsonify({id: buy_sell_point_by_id(id).to_json()})


# @app.route('/stock/api/calc', methods=['GET'])
def calc():
    calc_stage1()
    return "good"
    # return jsonify({id: select_stock.calc_stage1n()})

@app.route('/stock/api/pull', methods=['GET'])
def pull():
    all_id_list=get_all_id_list()
    get_data(loop=False,period=1, id_list=all_id_list)

    return "good"
    # return jsonify({id: select_stock.calc_stage1n()})



# todo:  buy历史时间, 推送, 图形界面
# todo: list作为set: 临时解决了



from flask_mail import Mail
from flask_mail import Message
mail=Mail(app)



@app.route('/stock/api/push/<set_name>/<thing>', methods=['GET'])
def push(set_name,thing):
    msg = Message('new push %s' % set_name,
                  sender=("lhr", "lhrkkk@mail.ustc.edu.cn"),
                  recipients="airhenry@gmail.com"
    )
    msg.body='''
Your set %s has a new push %s
'''% (set_name,thing)
    mail.send(msg)
    return "sended"














##############

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/stock/api/setlist/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

from flask import request

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

from flask import url_for

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True)
