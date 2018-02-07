#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json


def get_secret_key(s):
    with open("../config/token.json", 'r') as f:
        dic = json.load(f)
    return dic.get(s)
