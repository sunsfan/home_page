#! /usr/bin/env python
# -*- coding:utf-8 -*-

from db_service.db_helper import dbhelper
#from db_service.db_model import *
from datetime import datetime

# res = dbhelper.get_all_data('qrcode_record')
# print res

# res = dbhelper.get_data_by_index(1, 'goods_record')
# print res

#data = BANNER(index=3, image_url='a1', title='b1', description='c1')
# res = dbhelper.remove_data(5, 'banner_record')
# print res
d = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
filename = 'aaa.jpg'.split('.')[0] + '-' + d + '.' + 'aaa.jpg'.split('.')[1]
print filename