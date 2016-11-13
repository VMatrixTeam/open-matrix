
import model.base
import tornado.gen

from MySQLdb import escape_string

class Comment(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_comments_by_sid(sid):
        result = yield model.MatrixDB.query("select * from snippet_comment where sid = {0}".format(sid))
        for each in result:
            each.author = yield model.MatrixDB.get("select * from user where user_id = {0}".format(each.author))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def create_comment(content, sid, user_id):
        row_id = yield model.MatrixDB.execute("insert into snippet_comment (sid, content, author, createAt) values ({0}, '{1}', {2}, now())".format(sid, content, user_id))
        raise tornado.gen.Return(row_id)