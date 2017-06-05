'''
Created on May 26, 2017

@author: Marco Cornolti
'''

from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
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

@app.route('/edit_verdict')
def edit_verdict():
    return render_template('edit_verdict.html')


@app.route('/add_verdict')
def add_verdict():
    global al
    title = request.args.get('title')
    authority = request.args.get('authority')
    verdict_id = request.args.get('verdict_id')
    date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
    verdict_key = al.add_verdict(title, authority, verdict_id, date)
    return jsonify(result = "ok", verdict_key=verdict_key)


@app.route('/set_verdict_info')
def set_verdict_info():
    global al
    verdict_key = request.args.get('verdict_key')
    title = request.args.get('title')
    authority = request.args.get('authority')
    verdict_id = request.args.get('verdict_id')
    date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
    al.set_verdict_info(verdict_key, title, authority, verdict_id, date)
    return jsonify(result = "ok")


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

@app.route('/get_verdict_info')
def get_verdict_info():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    info = al.get_verdict_info(verdict_key)
    return jsonify(result = "ok", verdict_info = info)

@app.route('/get_all_verdicts')
def get_all_verdicts():
    global al
    info = al.get_all_verdicts()
    return jsonify(result = "ok", verdict_info = info)


@app.route('/get_actus_reus')
def get_actus_reus():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    actus_reus = al.get_actus_reus(verdict_key)
    return jsonify(result = "ok", actus_reus = actus_reus)

@app.route('/delete_actus_reus')
def delete_actus_reus():
    global al
    verdict_key = int(request.args.get('actus_reus_key'))
    al.delete_actus_reus(verdict_key)
    return jsonify(result = "ok")

@app.route('/add_natural_expression')
def add_natural_expression():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    expression = request.args.get('expression')
    al.add_natural_expression(verdict_key, expression)
    return jsonify(result = "ok")

@app.route('/get_natural_expressions')
def get_natural_expressions():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    natural_expressions = al.get_natural_expressions(verdict_key)
    return jsonify(result = "ok", natural_expressions = natural_expressions)

@app.route('/delete_natural_expression')
def delete_natural_expression():
    global al
    natural_expression_key = int(request.args.get('natural_expression_key'))
    al.delete_natural_expression(natural_expression_key)
    return jsonify(result = "ok")

@app.route('/delete_verdict')
def delete_verdict():
    global al
    verdict_key = int(request.args.get('verdict_key'))
    al.delete_verdict(verdict_key)
    return jsonify(result = "ok")


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
