from flask import jsonify, request
import os
from .run import app
from .optimizer_test import random_weights
# from flask_app import portfolio

@app.route('/')
def landing():
    test = {'this': 'works'}
    return jsonify(test)

@app.route('/api/test', methods=['GET','POST'])
def test():
    if request.method == 'GET':
        t = random_weights()
        return jsonify(t)
