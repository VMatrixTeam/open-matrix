
import model.base
import tornado.gen
from MySQLdb import escape_string

class Read(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_read_num_by_bid(bid):
        result = yield model.MatrixDB.get(
            """
                SELECT count(*) as count FROM blog_read where bid = {0}
            """.format(bid)
        )
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def get_user_read_by_bid_userid(bid, user_id):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def create_read(bid, user_id):
        pass
