from flask import Flask, jsonify, request
from models.leek import Leek
import mongoengine
import json
import sys
import math

app = Flask(__name__, static_folder='./webapp/', static_url_path='')

def get_filtered(ls, sigma, getter, distance):
    f = lambda x: math.exp(-0.5 * (x / sigma) ** 2)
    return (sum(getter(x2) * f(distance(x1, x2)) for x2 in ls) / sum(f(distance(x1, x2)) for x2 in ls) for x1 in ls)

def get_levels():
    result = Leek._get_collection().aggregate([
        {'$project': {
            '_id': 0, 'level': 1, 'strength': 1, 'agility': 1,
            'life': 1,
            # 'life': {'$divide': [
            #     {'$subtract': [
            #         {'$subtract': [
            #             {'$subtract': [
            #                 '$life',
            #                 {'$divide': [
            #                     '$level',
            #                     5
            #                 ]}
            #             ]},
            #             {'$cond': {
            #                 'if': {'$gt': ['$level', 200]},
            #                 'then': {'$divide': [
            #                     {'$subtract': [
            #                         '$level',
            #                         200
            #                     ]},
            #                     5
            #                 ]},
            #                 'else': 0
            #             }}
            #         ]},
            #         50
            #     ]},
            #     3
            # ]},
            'ratio': {'$divide': [
                '$nb_victory',
                {'$add': [
                    '$nb_defeat',
                    {'$add': [
                        '$nb_draw',
                        1
                    ]}
                ]}
            ]}
        }},
        {'$group': {
            '_id': '$level',
            'str': {'$sum': {'$multiply': ['$strength', '$ratio']}},
            'agi': {'$sum': {'$multiply': ['$agility', '$ratio']}},
            'life': {'$sum': {'$multiply': ['$life', '$ratio']}},
            'ratio': {'$sum': '$ratio'},
        }},
        {'$project': {
            '_id': 0,
            'level': '$_id',
            'str': {'$divide': ['$str', '$ratio']},
            'agi': {'$divide': ['$agi', '$ratio']},
            'life': {'$divide': ['$life', '$ratio']},
        }},
        {'$sort': {'level': 1}}
    ])
    return result['result']

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/levels/')
def api_get_levels():
    return jsonify({'levels': get_levels()})

@app.route('/api/levels/filtered')
def api_get_levels_filtered():
    sigma = request.args.get('sigma')
    if sigma is None:
        sigma = 1.0
    sigma = float(sigma)

    result = get_levels()
    distance = lambda x, y: abs(x['level'] - y['level'])
    strength = get_filtered(result, sigma, getter=lambda r: r['str'], distance=distance)
    agility = get_filtered(result, sigma, getter=lambda r: r['agi'], distance=distance)
    life = get_filtered(result, sigma, getter=lambda r: r['life'], distance=distance)
    output = [{'level': r['level'], 'str': s, 'agi': a, 'life': l}
        for r, s, a, l in zip(result, strength, agility, life)]
    return jsonify({'levels': output})

if __name__ == '__main__':
    mongoengine.connect('leekdb')
    app.run(host='0.0.0.0',
        debug='--debug' in sys.argv,
        port=9001,
        threaded=True)
