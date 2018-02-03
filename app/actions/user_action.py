#! /usr/bin/env python
# -*- coding:utf-8 -*-

from db_service.db_model import *
from db_service.db_helper import dbhelper
from utils.hash_utils import HashUtils


class UserAction(object):

    @classmethod
    def user_logon(cls, data):
        username = data.get(u'username')
        password = data.get(u'password')
        password_hash = HashUtils.get_key(password)
        token_id = HashUtils.uuid()
        user = USER(username=username, password_hash=password_hash, token_id=token_id)
        dbhelper.add_user_data(user)

    @classmethod
    def user_auth(cls, data):
        username = data.get(u'username')
        password = data.get(u'password')
        password_hash = HashUtils.get_key(password)
        old_hash = dbhelper.get_password_hash_by_username(username)
        if old_hash == password_hash:
            return dbhelper.get_token_id_by_username(username)
        else:
            raise Exception('user auth failed')
