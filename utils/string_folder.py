#!/usr/bin/env python
# -*- coding:utf-8 -*-


class StringFolder(object):
    def __init__(self):
        self.unicode_map = {}

    def fold_string(self, s):
        if not isinstance(s, basestring):
            return s
        try:
            return intern(str(s))
        except UnicodeEncodeError:
            pass
        t = self.unicode_map.get(s, None)
        if t is None:
            t = self.unicode_map[s] = s
        return t