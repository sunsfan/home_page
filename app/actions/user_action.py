#! /usr/bin/env python
# -*- coding:utf-8 -*-

from db_service.db_model import *
from db_service.db_helper import dbhelper
from utils.hash_utils import HashUtils
from flask import abort


class UserAction(object):

    @classmethod
    def login_user(cls, data):
        username = data.get(u'username')
        password = data.get(u'password')
        password_hash = HashUtils.get_key(password)
        if username is None or password is None:
            abort(400)
        user = dbhelper.get_user_by_username(username)
        if not user:
            abort(400)
        if user.password_hash == password_hash:
            return user.username, user.token
        else:
            abort(401)

    @classmethod
    def update_user(cls, data):
        username = data.get(u'username')
        password = data.get(u'password')
        token = data.get(u'token')
        password_hash = HashUtils.get_key(password)
        token_hash = HashUtils.get_key(token)
        user = dbhelper.get_user_by_username(username)
        if user:
            dbhelper.update_user_data(user, password_hash=password_hash, token_hash=token_hash)
        else:
            user = USER(username=username, password_hash=password_hash, token_hash=token_hash)
            dbhelper.add_user_data(user)
        return username
