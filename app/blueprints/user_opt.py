#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from flask import Blueprint, request, make_response, jsonify
from app.actions.user_action import UserAction


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/logon', methods=['POST'])
def user_logon():
    body = request.get_data()
    try:
        req_data = json.loads(body)
        UserAction.user_logon(req_data)
        resp = '{"status": 0, "user": "%s"}' % (req_data.get(u'username'))
        return resp, 200
    except Exception as e:
        return make_response(jsonify({'status': 400, 'message': 'Error msg:%s' % e}), 400)


@user_blueprint.route('/login', methods=['POST'])
def user_login():
    body = request.get_data()
    try:
        req_data = json.loads(body)
        result = UserAction.user_auth(req_data)
        resp = '{"status": 0, "token": "%s"}' % result
        return resp, 200
    except Exception as e:
        return make_response(jsonify({'status': 400, 'message': 'Error msg:%s' % e}), 400)
