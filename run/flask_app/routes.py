from flask import jsonify, request
import os
from .run import app
from .optimizer_test import random_weights, ret_vol_allos, historical_chart
# from flask_app import portfolio

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
        t = ret_vol_allos(0.90)
        return jsonify(t)
    elif request.method == 'POST':
        port_makeup = request.json['eq_pct']
        allos = ret_vol_allos(port_makeup)
        return jsonify(allos)

@app.route('/allocated/chart', methods=['GET','POST'])
def chart():
    if request.method == 'GET':
        chart = historical_chart(0.90)
        return jsonify(chart)
