'''
Created on May 26, 2017

@author: Marco Cornolti
'''

from argparse import ArgumentParser
from collections import Counter
from flask import Flask, jsonify, request, redirect, render_template
import flask
import logging
import os
import re
import sys

from autolex import Autolex


app = Flask(__name__,
            static_folder=os.path.join("..", "..", "..", "resources", "web", "static"),
            static_path="/static",
            template_folder=os.path.join("..", "..", "..", "resources", "web", "templates")
            )

@app.route('/')
@app.route('/index.html')
@app.route('/list_verdicts')
def index():
    return render_template('list_verdicts.html')


@app.route('/add_verdict')
def add_verdict():
    global al
    title = request.args.get('title')
    authority = request.args.get('authority')
    verdict_id = request.args.get('verdict_id')
    date = request.args.get('date')
    verdict_key = al.add_verdict(title, authority, verdict_id, date)
    return jsonify(result = "ok", verdict_key=verdict_key)


@app.route('/set_verdict_description')
def set_verdict_description():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    description = request.args.get('description')
    al.set_verdict_description(verdict_key, description)
    return jsonify(result = "ok")


@app.route('/add_actus_reus')
def add_actus_reus():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    description = request.args.get('description')
    law = request.args.get('law')
    al.add_actus_reus(verdict_key, description, law)
    return jsonify(result = "ok")


@app.route('/add_natural_expression')
def add_natural_expression():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    expression = request.args.get('expression')
    al.add_natural_expression(verdict_key, expression)
    return jsonify(result = "ok")

@app.route('/get_verdicts_info')
def get_verdicts_info():
    global al
    info = al.get_verdicts_info()
    return jsonify(result = "ok", verdict_info = info)


def main():
    global al
    parser = ArgumentParser()
    parser.add_argument("-s", "--storage_db", required=True, action="store", help="Storage DB file")
    args = parser.parse_args()

    al = Autolex(args.storage_db)
    return app.run(host="0.0.0.0")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    sys.exit(main())
