#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from flask import Blueprint, request, make_response, jsonify
from app.actions.data_action import DataAction

data_blueprint = Blueprint('data', __name__)


@data_blueprint.route('/getdata', methods=['POST'])
def get_data():
    body = request.get_data()
    try:
        req_data = json.loads(body)
        result = DataAction.get_data(req_data)
        return make_response(jsonify({'code': 0, 'data': result}), 200)
    except Exception as e:
        return make_response(jsonify({'status': 400, 'message': 'Error msg:%s' % e}), 400)


@data_blueprint.route('/updatedata', methods=['POST'])
def update_data():
    body = request.get_data()
    try:
        req_data = json.loads(body)
        result = DataAction.update_data(req_data)
        return make_response(jsonify({'code': 0, 'data': result}), 200)
    except Exception as e:
        return make_response(jsonify({'status': 400, 'message': 'Error msg:%s' % e}), 400)