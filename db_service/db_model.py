#! /usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, LargeBinary, Integer, Float
import json
from werkzeug.security import generate_password_hash, check_password_hash
from mysql_config import MYSQL
from sqlalchemy import create_engine, exc, event, select

Base = declarative_base()


class BANNER(Base):

    __tablename__ = MYSQL.MYSQL_TABLE_BANNER

    index = Column(Integer, primary_key=True, autoincrement=False)
    image = Column(String(100))
    title = Column(String(20))
    description = Column(String(255))

    def __repr__(self):
        jstr = {"index": self.index, "image": self.image, "title": self.title, "description": self.description}
        return json.dumps(jstr)


class GOODS(Base):

    __tablename__ = MYSQL.MYSQL_TABLE_GOODS

    index = Column(Integer, primary_key=True, autoincrement=False)
    image = Column(String(100))
    title = Column(String(20))
    description = Column(String(255))
    price = Column(Float)
    status = Column(Integer)
    priority = Column(Integer)

    def __repr__(self):
        jstr = {"index": self.index, "image": self.image, "title": self.title, "description": self.description,
                "price": self.price, "status": self.status, "priority": self.priority}
        return json.dumps(jstr)


class QRCODE(Base):

    __tablename__ = MYSQL.MYSQL_TABLE_QRCODE

    index = Column(Integer, primary_key=True, autoincrement=False)
    image = Column(String(100))

    def __repr__(self):
        jstr = {"index": self.index, "image": self.image}
        return json.dumps(jstr)


class USER(Base):
    __tablename__ = MYSQL.MYSQL_TABLE_USER

    username = Column(String(20), primary_key=True, unique=True)
    password_hash = Column(String(128))
    token_id = Column(String(128))
    
    def __repr__(self):
        jstr = {"username": self.username, "password": self.password}
        return json.dumps(jstr)

# MYSQL_URI = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(MYSQL.MYSQL_USERNAME,
#                         MYSQL.MYSQL_PASSWORD, MYSQL.MYSQL_HOST, MYSQL.MYSQL_PORT, MYSQL.MYSQL_DB)
# engine = create_engine(MYSQL_URI, pool_size=10, pool_recycle=3600, max_overflow=5)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)