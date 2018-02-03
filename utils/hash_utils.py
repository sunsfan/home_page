#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import uuid as uid


class HashUtils(object):

    @classmethod
    def get_key(cls, src):
        m2 = hashlib.md5()
        m2.update(src)
        return m2.hexdigest()

    @classmethod
    def uuid(cls):
        return str(uid.uuid1()).replace("-", "")

