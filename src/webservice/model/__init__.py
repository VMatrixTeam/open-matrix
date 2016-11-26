#coding:utf-8

import files
import user

from tornado import gen

import config

import asynctorndb

CONFIG = config.get_config()

MatrixDB_config = dict(
    user=CONFIG['database']['openmatrix']['username'],
    passwd=CONFIG['database']['openmatrix']['password'],
    database=CONFIG['database']['openmatrix']['database'],
    host=CONFIG['database']['openmatrix']['host'],
    port=CONFIG['database']['openmatrix']['port'],
    charset=CONFIG['database']['openmatrix']['charset']
)

class MatrixDB(object):
    @staticmethod
    @gen.coroutine
    def query(sql):
        db = asynctorndb.Connect(**MatrixDB_config)
        yield db.connect()
        result = yield db.query(sql)
        yield db.close()
        raise gen.Return(result)

    @staticmethod
    @gen.coroutine
    def execute(sql):
        db = asynctorndb.Connect(**MatrixDB_config)
        yield db.connect()
        result = yield db.execute(sql)
        yield db.close()
        raise gen.Return(result)

    @staticmethod
    @gen.coroutine
    def get(sql):
        db = asynctorndb.Connect(**MatrixDB_config)
        yield db.connect()
        result = yield db.get(sql)
        yield db.close()
        raise gen.Return(result)
