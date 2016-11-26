
import model
import tornado.gen

from MySQLdb import escape_string

class Praise(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_praises_by_sid(sid):
        result = yield model.MatrixDB.query("select * from snippet_praise where sid = {0}".format(sid))
        # db = model.base.get_matrixDB()
        # yield db.connect()
        # for each in result:
        #     each.author = yield db.get("select * from user where user_id = {0}".format(each.user_id))
        # db.close()
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_praises_count_by_sid(sid):
        result = yield model.MatrixDB.get("select count(*) as count from snippet_praise where sid = {0}".format(sid))
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def get_praises_count_by_sid_user_id(sid, user_id):
        result = yield model.MatrixDB.get("select count(*) as count from snippet_praise where sid = {0} and user_id = {1}".format(sid, user_id))
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def create_praise(sid, user_id):
        row_id = yield model.MatrixDB.execute("insert into snippet_praise (user_id, sid, createAt) values ({0}, {1}, now())".format(user_id, sid))
        raise tornado.gen.Return(row_id)
