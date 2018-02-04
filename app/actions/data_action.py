#! /usr/bin/env python
# -*- coding:utf-8 -*-

from db_service.db_model import *
from db_service.db_helper import dbhelper

TOKEN = ''


def check(token):
    if token == TOKEN:
        pass
    else:
        raise Exception('token auth failed')


class DataAction(object):

    @classmethod
    def get_data(cls, data):
        data_type = data.get(u'dataType')
        if data_type == 0:
            return dbhelper.get_all_data('banner_record')
        elif data_type == 2:
            return dbhelper.get_all_data('qrcode_record')
        else:
            page = data.get(u'page')
            return dbhelper.get_all_data_by_page(page)


    @classmethod
    def update_data(cls, data):
        data_type = data.get(u'dataType')
        action_type = data.get(u'actionType')
        # token_id = data.get(u'token')
        # check(token_id)
        db_data = data.get(u'data')
        # print 'db_data is {type}'.format(type=db_data)
        if data_type == 0:
            banner_data = BANNER(index=db_data.get(u'index'), image=db_data.get(u'image'),
                                 title=db_data.get(u'title'), description=db_data.get(u'description'))
            if action_type == 0:
                dbhelper.insert_data(banner_data, 'banner_record')
            elif action_type == 1:
                dbhelper.update_data(banner_data, 'banner_record')
            else:
                dbhelper.remove_data(banner_data.index, 'banner_record')
        elif data_type == 1:
            goods_data = GOODS(index=db_data.get(u'index'), image=db_data.get(u'image'),
                               title=db_data.get(u'title'), description=db_data.get(u'description'),
                               price=db_data.get(u'price'), status=db_data.get(u'status'),
                               priority=db_data.get(u'priority'))
            if action_type == 0:
                dbhelper.insert_data(goods_data, 'goods_record')
            elif action_type == 1:
                dbhelper.update_data(goods_data, 'goods_record')
            else:
                dbhelper.remove_data(goods_data.index, 'goods_record')
        else:
            qrcode_data = QRCODE(index=db_data.get(u'index'), image=db_data.get(u'image'))
            if action_type == 0:
                dbhelper.insert_data(qrcode_data, 'qrcode_record')
            elif action_type == 1:
                dbhelper.update_data(qrcode_data, 'qrcode_record')
            else:
                dbhelper.remove_data(qrcode_data.index, 'qrcode_record')

