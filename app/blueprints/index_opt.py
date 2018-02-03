#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, render_template


index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/index', methods=['GET'])
def index_opt():
    return render_template("index.html", title="HomePage", user="amyFox")