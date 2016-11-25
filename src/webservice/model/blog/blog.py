# coding=utf-8

import model
import tornado.gen
from MySQLdb import escape_string

class Blog(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_blog_by_bid(bid):
        result = yield model.MatrixDB.get("select * from blog_blog where bid = {0}".format(bid))
        raise tornado.gen.Return(result)

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
    def create_blog(author_id, title, brief, content):
        content = content.replace("%", "%%")
        row_id = yield model.MatrixDB.execute("insert into blog_blog (author, title, brief, createAt, updateAt, content) values ({0}, '{1}', '{2}', now(), now(), '{3}')".format(author_id, escape_string(title), escape_string(brief), escape_string(content)))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def delete_blog_by_bid(bid):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def update_blog_by_bid(bid, title, brief, content):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def get_blogs_by_uid_latest_100(user_id):
        result = yield model.MatrixDB.query("select * from blog_blog where author = {0} order by createAt desc limit 0, 100".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_top_blogs_by_count(count):
        result = yield model.MatrixDB.query(
            """
                select bb.bid as bid, max(bb.author) as author, max(bb.title) as title, max(bb.brief) as brief, max(bb.createAt) as createAt, max(bb.updateAt) as updateAt, max(bb.content) as content, count(*) as count 
                from blog_blog bb left join blog_praise bp on bb.bid = bp.bid 
                group by bb.bid 
                order by count desc 
                limit 0, {0}
            """.format(count)
        )
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_author_other_blogs_by_uid(user_id, bid):
        result = yield model.MatrixDB.query("select * from blog_blog where author = {0} and bid != {1}".format(user_id, bid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_related_blogs_by_bid(bid):
        result = yield model.MatrixDB.query("select * from blog_blog where bid = {0}".format(bid))
        raise tornado.gen.Return(result)
