# -*- coding: utf-8 -*-

import json
from functools import wraps
from flask import jsonify, request
from db_service.db_helper import dbhelper
from utils.hash_utils import HashUtils


class BaseAuth(object):

    @staticmethod
    def get_authorization(username):
        return dbhelper.get_token_hash_by_username(username)

    def authorize(self, realf):
        @wraps(realf)
        def decorated_function(*args, **kws):
            body = request.get_data()
            req_data = json.loads(body)
            username = req_data.get(u'username')
            authorization = req_data.get(u'authorization')
            if not username or not authorization:
                return jsonify({"status": 401, "description": u"认证信息缺失"}), 401
            verify_auth = self.get_authorization(username)
            if not verify_auth == authorization:
                return jsonify({"status": 401, "description": u"没有访问权限"}), 401
            return realf(*args, **kws)

        return decorated_function


ba = BaseAuth()
