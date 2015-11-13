#!/usr/bin/env python
from flask import Flask, jsonify
import os
import time
from random import gauss
from json import load

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), "configuration.json")) as f:
    configuration = load(f)

bytecount = configuration['bytecount']
bytecount_mean = bytecount['mean']
bytecount_stdev = bytecount['stdev']

duration = configuration['duration']
duration_mean = duration['mean']
duration_stdev = duration['stdev']

number = configuration['number']
number_mean = number['mean']
number_stdev = number['stdev']

percent = configuration['percent']
percent_mean = percent['mean']
percent_stdev = percent['stdev']


def get_performance_metrics():
    return {
        "timestamp": int(time.time()),
        "results":
            [
                {
                    'name': u'bytecount',
                    'value': int(gauss(bytecount_mean, bytecount_stdev))
                },
                {
                    'name': u'duration',
                    'value': round(gauss(duration_mean, duration_stdev), 2)
                },
                {
                    'name': u'number',
                    'value': round(gauss(number_mean, number_stdev), 1)
                },
                {
                    'name': u'percent',
                    'value': round(gauss(percent_mean, percent_stdev), 3)
                }
            ]
    }


@app.route('/api/v1/performance', methods=['GET'])
def get_tasks():
    return jsonify(get_performance_metrics())


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
