
import model.base
import tornado.gen
from MySQLdb import escape_string

class Comment(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_comment_num_by_bid(bid):
        result = yield model.MatrixDB.get(
            """
                SELECT count(*) as count FROM blog_comment where bid = {0}
            """.format(bid)
        )
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def get_comments_by_bid(bid):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def create_comment(author_id, bid, content):
        pass

    @staticmethod
    @tornado.gen.coroutine
    def delete_comment_by_cid(cid):
        pass
