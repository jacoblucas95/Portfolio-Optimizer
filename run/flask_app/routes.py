from flask import jsonify, request
import json
import os
from .run import app
from .optimizer import random_weights, ret_vol_allos, historical_chart
from .new_optimizations import ret_vol_allos_dummy

@app.route('/')
def landing():
    test = {'this': 'works'}
    return jsonify(test)

@app.route('/weights/random', methods=['GET','POST'])
def random():
    if request.method == 'GET':
        t = random_weights()
        return jsonify(t)

@app.route('/weights/optimize', methods=['GET','POST'])
def optimize():
    if request.method == 'GET':
        port = 0.9
        vol = 3
        t = ret_vol_allos(port, vol)
        return jsonify(t)
    elif request.method == 'POST':
        # port_makeup = request.json['eq_pct']
        port_makeup = 0.9
        vol = request.json['vol'] - 1
        allos = ret_vol_allos(port_makeup, vol)
        return jsonify(allos)

@app.route('/allocated/chart', methods=['GET','POST'])
def chart():
    if request.method == 'GET':
        chart = historical_chart(0.90,3)
        return jsonify(chart)
    elif request.method == 'POST':
        vol = request.json['vol'] - 1
        chart = historical_chart(0.90, vol)
        return jsonify(chart)

@app.route('/hardcoded/weights')
def hardcode():
    x = [{'allocations': [{'ticker':"BND", 'weight': 1.2211568505617938e-16},
        {'ticker': "SCHP", 'weight': 1.745578096439442e-17}]
        },
        {'extraInfo':[
            {'sharpe':1},
            {'volatility': 0.5},
            {'return': 0.07}
        ]}]
    return jsonify(x)

@app.route('/optimized/personal/holding',methods=['GET','POST'])
def personal_holding():
    if request.method == 'GET':
        port = 0.9
        vol = 3
        ticker = 'C'
        dummy_allos = ret_vol_allos_dummy(port,vol,ticker)
        return jsonify(dummy_allos)
    elif request.method == 'POST':
        port = 0.9
        vol = request.json['vol'] - 1
        ticker = request.json['ticker']
        allos = ret_vol_allos_dummy(port,vol,ticker)
        return jsonify(allos)

@app.route('/personal/allocated/chart')
def personal_chart():
    if request.method == 'GET':
        chart = historical_chart(0.90,3)
        return jsonify(chart)
    elif request.method == 'POST':
        vol = request.json['vol'] - 1
        chart = historical_chart(0.90, vol)
        return jsonify(chart)

@app.route('/faster/optimized/weights', methods=['GET','POST'])
def faster():
    if request.method == 'GET':
        with open('data.json') as json_file:
            data = json.load(json_file)
        return jsonify(data[1])
    elif request.method == 'POST':
        vol = request.json['vol'] - 1
        with open('data.json') as json_file:
            data = json.load(json_file)
        vol_data = data[vol]
        return jsonify(vol_data)
#
# @app.route('/faster/personal/optimized/weights', methods=['GET','POST'])
# def personal_faster():
#     if request.method == 'GET':
#         with open('personal_data.json') as json_file:
#             data = json.load(json_file)
#         return jsonify(data[1])
#     elif request.method == 'POST':
#         vol = request.json['vol'] - 1
#         ticker = request.json['ticker']
#         with open('personal_data.json') as json_file:
#             data = json.load(json_file)
#         vol_data = data[vol]
#         vol_data[0]['allocations'][ticker] = vol_data[0]['allocations']['C']
#         # vol_data[0]['allocations'].pop('C')
#         return jsonify(vol_data)
