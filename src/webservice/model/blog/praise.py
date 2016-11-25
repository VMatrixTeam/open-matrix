
import model
import tornado.gen
from MySQLdb import escape_string

class Praise(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_praise_num_by_bid(bid):
        result = yield model.MatrixDB.get(
            """
                SELECT count(*) as count FROM blog_praise where bid = {0}
            """.format(bid)
        )
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def get_user_praised_by_bid_userid(bid, user_id):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def create_praise(bid, user_id):
        row_id = yield model.MatrixDB.execute("insert into blog_praise (author, bid, createAt) values ({0}, {1}, now())".format(user_id, bid))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def delete_praise(bid, user_id):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def get_praises_count_by_bid_user_id(bid, user_id):
        result = yield model.MatrixDB.get("select count(*) as count from blog_praise where bid = {0} and author = {1}".format(bid, user_id))
        raise tornado.gen.Return(result.count)
