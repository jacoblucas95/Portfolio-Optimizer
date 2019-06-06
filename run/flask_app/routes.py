from flask import jsonify, request
import os
from .run import app
from flask_app import portfolio

@app.route('/')
def landing():
    return jsonify(portfolio())
