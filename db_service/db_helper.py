#! /usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import BANNER, GOODS, QRCODE, USER
from mysql_config import MYSQL, GLOBLE
from utils.string_folder import StringFolder
from exception import MYSQLError


class DBHelper(object):

    def __init__(self):
        self.MYSQL_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(MYSQL.MYSQL_USERNAME,
                        MYSQL.MYSQL_PASSWORD, MYSQL.MYSQL_HOST, MYSQL.MYSQL_PORT, MYSQL.MYSQL_DB)
        self.engine = create_engine(self.MYSQL_URI, pool_size=10, pool_recycle=3600, max_overflow=5)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # 根据表名获得所有数据
    def get_all_data(self, table):
        dics = []
        with self.engine.connect() as connection:
            if 'banner_record' == table:
                rows = connection.execution_options(stream_results=True).execute("select `index`, image, title, \
                description from {0}".format(MYSQL.MYSQL_TABLE_BANNER))
                for dic in self.get_banner_by_step(rows):
                    dics.append(dic)
            elif 'qrcode_record' == table:
                rows = connection.execution_options(stream_results=True).execute("select `index`, image from {0}"
                .format(MYSQL.MYSQL_TABLE_QRCODE))
                for dic in self.get_qrcode_by_step(rows):
                    dics.append(dic)
            else:
                raise MYSQLError('table name incorrect')
            rows.close()
            self.session.close()
        return dics

    # 根据表名获得指定页所有数据
    def get_all_data_by_page(self, page):
        dics = []
        begin = (page - 1) * 20 + 1
        end = page * 20
        with self.engine.connect() as connection:
            rows = connection.execution_options(stream_results=True).execute("select `index`, image, title, \
            description, price, status, priority from {0} where `index` BETWEEN {1} AND {2}".format(MYSQL.MYSQL_TABLE_GOODS, begin, end))
            for dic in self.get_goods_by_step(rows):
                dics.append(dic)
        return dics

    # banner数据生成器
    def get_banner_by_step(self, results):
        folder = StringFolder()
        for row in results:
            yield {folder.fold_string("index"): folder.fold_string(row[0]),
                   folder.fold_string("image"): folder.fold_string(row[1]),
                   folder.fold_string("title"): folder.fold_string(row[2]),
                   folder.fold_string("description"): folder.fold_string(row[3]),
                   }

    # goods数据生成器
    def get_goods_by_step(self, results):
        folder = StringFolder()
        for row in results:
            yield {folder.fold_string("index"): folder.fold_string(row[0]),
                   folder.fold_string("image"): folder.fold_string(row[1]),
                   folder.fold_string("title"): folder.fold_string(row[2]),
                   folder.fold_string("description"): folder.fold_string(row[3]),
                   folder.fold_string("price"): folder.fold_string(row[4]),
                   folder.fold_string("status"): folder.fold_string(row[5]),
                   folder.fold_string("priority"): folder.fold_string(row[6]),
                   }

    # qrcode数据生成器
    def get_qrcode_by_step(self, results):
        folder = StringFolder()
        for row in results:
            yield {folder.fold_string("index"): folder.fold_string(row[0]),
                   folder.fold_string("image"): folder.fold_string(row[1]),
                   }

    # 根据序号获得对应数据
    def get_data_by_index(self, index, table):
        if 'banner_record' == table:
            data = self.session.query(BANNER).filter(BANNER.index == index).first()
        elif 'goods_record' == table:
            data = self.session.query(GOODS).filter(GOODS.index == index).first()
        elif 'qrcode_record' == table:
            data = self.session.query(QRCODE).filter(QRCODE.index == index).first()
        else:
            data = None
        return data

    # 更新数据（根据序号更新，没有老数据则插入，有老数据则更新）
    def update_data(self, data, table):
        old = self.get_data_by_index(data.index, table)
        if not old:
            if 'banner_record' == table:
                banner = BANNER(index=data.index, image=data.image, title=data.title, description=data.description)
                try:
                    self.session.add(banner)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                return GLOBLE.OK
            elif 'goods_record' == table:
                goods = GOODS(index=data.index, image=data.image, title=data.title, description=data.description,
                              price=data.price, status=data.status, priority=data.priority)
                try:
                    self.session.add(goods)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                return GLOBLE.OK
            elif 'qrcode_record' == table:
                qrcode = QRCODE(index=data.index, image=data.image)
                try:
                    self.session.add(qrcode)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                return GLOBLE.OK
            else:
                return GLOBLE.NOT_OK
        else:
            if 'banner_record' == table:
                old.image = data.image
                old.title = data.title
                old.description = data.description
                try:
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                return GLOBLE.OK
            elif 'goods_record' == table:
                old.image = data.image
                old.title = data.title
                old.description = data.description
                old.price = data.price
                old.status = data.status
                old.priority = data.priority
                try:
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                return GLOBLE.OK
            elif 'qrcode_record' == table:
                old.image = data.image
                try:
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                return GLOBLE.OK
            else:
                return GLOBLE.NOT_OK

    # 删除数据
    def delete_data(self, index, table):
        data = self.get_data_by_index(index, table)
        try:
            self.session.delete(data)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
        return GLOBLE.OK

    # 获取序号大于等于特定值的所有数据
    def get_datas_over_or_equal_index(self, index, table):
        if 'banner_record' == table:
            data = self.session.query(BANNER).filter(BANNER.index >= index).all()
        elif 'goods_record' == table:
            data = self.session.query(GOODS).filter(GOODS.index >= index).all()
        elif 'qrcode_record' == table:
            data = self.session.query(QRCODE).filter(QRCODE.index >= index).all()
        else:
            data = None
        return data

    # 获取序号大于特定值的所有数据
    def get_datas_over_index(self, index, table):
        if 'banner_record' == table:
            data = self.session.query(BANNER).filter(BANNER.index > index).all()
        elif 'goods_record' == table:
            data = self.session.query(GOODS).filter(GOODS.index > index).all()
        elif 'qrcode_record' == table:
            data = self.session.query(QRCODE).filter(QRCODE.index > index).all()
        else:
            data = None
        return data

    # 插入数据，序号大于等于此数据序号的所有数据序号加1
    def insert_data(self, data, table):
        data_list = self.get_datas_over_or_equal_index(data.index, table)
        data_list = data_list[::-1]
        for l in data_list:
            l.index = l.index + 1
            if 'banner_record' == table:
                d = BANNER(index=l.index, image=l.image, title=l.title, description=l.description)
            elif 'goods_record' == table:
                d = GOODS(index=l.index, image=l.image, title=l.title, description=l.description,
                              price=l.price, status=l.status, priority=l.priority)
            elif 'qrcode_record' == table:
                d = QRCODE(index=l.index, image=l.image)
            else:
                return GLOBLE.NOT_OK
            self.update_data(d, table)
        self.update_data(data, table)
        return GLOBLE.OK

    # 删除指定序号位置的数据，序号大于此值的所有数据序号减1
    def remove_data(self, index, table):
        self.delete_data(index, table)
        data_list = self.get_datas_over_index(index, table)
        for l in data_list:
            l.index = l.index - 1
            if 'banner_record' == table:
                d = BANNER(index=l.index, image=l.image, title=l.title, description=l.description)
            elif 'goods_record' == table:
                d = GOODS(index=l.index, image=l.image, title=l.title, description=l.description,
                              price=l.price, status=l.status, priority=l.priority)
            elif 'qrcode_record' == table:
                d = QRCODE(index=l.index, image=l.image)
            else:
                return GLOBLE.NOT_OK
            self.update_data(d, table)
        return GLOBLE.OK

    # 新增管理员用户
    def add_user_data(self, user):
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
        return GLOBLE.OK

    # 根据用户名查找用户
    def get_user_by_username(self, username):
        data = self.session.query(USER).filter(USER.username == username).first()
        return data

    # 根据用户名获取口令哈希
    def get_password_hash_by_username(self, username):
        data = self.session.query(USER).filter(USER.username == username).first()
        return data.password_hash

    # 根据用户名获取token
    def get_token_by_username(self, username):
        data = self.session.query(USER).filter(USER.username == username).first()
        return data.token

    # 更改用户密码和令牌
    def update_user_data(self, user, password_hash, token):
        user.password_hash = password_hash
        user.token_hash = token
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
        return GLOBLE.OK


dbhelper = DBHelper()




# new_banner = BANNER(index=1, image='http:111.com', title='标题一', description='描述一')
# session.add(new_banner)
# session.commit()
# session.close()
# data = dbhelper.get_all_data('banner_record')
# print data
