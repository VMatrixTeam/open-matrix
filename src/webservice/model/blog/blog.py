# coding=utf-8

import model
import tornado.gen
from MySQLdb import escape_string

class Blog(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_blog_by_bid(bid):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def get_blog_list(id_from, count):
        result = yield model.MatrixDB.query(
            """
                SELECT * FROM blog_blog ORDER BY updateAt LIMIT {0}, {1}
            """.format(
                id_from, count
            )
        )
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_blog_num():
        result = yield model.MatrixDB.get(
            """
                SELECT count(*) as count FROM blog_blog
            """
        )
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def create_blog(author_id, tittle, brief, content):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def delete_blog_by_bid(bid):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def update_blog_by_bid(bid, tittle, brief, content):
        pass
