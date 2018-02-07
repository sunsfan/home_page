#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from flask import Blueprint, request, jsonify
from app.actions.user_action import UserAction
from flask.ext.httpauth import HTTPBasicAuth


user_blueprint = Blueprint('user', __name__)
auth = HTTPBasicAuth()


@user_blueprint.route('/users', methods=['POST'])
def login_user():
    body = request.get_data()
    req_data = json.loads(body)
    res, token = UserAction.login_user(req_data)
    return jsonify({"status": 0, "username": res, "token": token}), 200


@user_blueprint.route('/users', methods=['PUT'])
def update_user():
    body = request.get_data()
    req_data = json.loads(body)
    res = UserAction.update_user(req_data)
    return jsonify({"status": 0, "username": res}), 200

# @user_blueprint.route('/login', methods=['POST'])
# def user_login():
#     body = request.get_data()
#     try:
#         req_data = json.loads(body)
#         result = UserAction.user_auth(req_data)
#         resp = '{"status": 0, "token": "%s"}' % result
#         return resp, 200
#     except Exception as e:
#         return make_response(jsonify({'status': 400, 'message': 'Error msg:%s' % e}), 400)
