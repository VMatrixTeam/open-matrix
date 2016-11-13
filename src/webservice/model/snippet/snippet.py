import model.base
import tornado.gen
import json

from MySQLdb import escape_string

class Snippet(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_snippets(id_from, count):
        result = yield model.MatrixDB.query("select * from snippet_snippet order by createAt desc limit {0}, {1}".format(id_from, count))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_snippet_count():
        result = yield model.MatrixDB.get("select count(*) as count from snippet_snippet")
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def get_top_snippets_by_count(count):
        result = yield model.MatrixDB.query("\
            select ss.sid as sid, max(ss.author) as author, max(ss.createAt) as createAt, max(ss.content) as content, max(ss.code) as code, max(ss.pictures) as pictures, count(*) as count \
            from snippet_snippet ss left join snippet_praise sp on ss.sid = sp.sid \
            group by ss.sid \
            order by count desc \
            limit 0, {0}".format(count))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_snippets_by_uid_latest_count(user_id, count):
        result = yield model.MatrixDB.query("select * from snippet_snippet where author = {0} order by createAt desc limit 0, {1}".format(user_id, count))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_snippet_by_sid(sid):
        result = yield model.MatrixDB.get("select * from snippet_snippet where sid = {0}".format(sid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def create_snippet(content, code, pictures, user_id):
        row_id = yield model.MatrixDB.execute("insert into snippet_snippet (author, createAt, content, code, pictures) values ({0}, now(), '{1}', '{2}', '{3}')".format(user_id, escape_string(content), escape_string(code), escape_string(json.dumps(pictures))))
        raise tornado.gen.Return(row_id)
