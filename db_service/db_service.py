#! /usr/bin/env python
# -*- coding:utf-8 -*-

from db_helper import dbhelper

class DBService(object):


    def update_commit(self):
        return dbhelper.update_commit()

    def update_rollback(self):
        return dbhelper.update_rollback()

    def update_data(self, data):
        res = dbhelper.update_data(data)
        return res

dbservice = DBService()