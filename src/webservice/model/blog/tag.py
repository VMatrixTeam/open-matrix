
import model
import tornado.gen

from MySQLdb import escape_string

class Tag(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_tags_by_bid(bid):
        result = yield model.MatrixDB.query("select * from blog_tag where bid = {0} limit 0, 5".format(bid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_tags_like_name(name):
        result = yield model.MatrixDB.query("select tag, count(*) as count from blog_tag where tag like '%%{0}%%'group by tag order by count desc limit 0, 5".format(escape_string(name)))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def create_tag(bid, tag):
        tag = tag.replace("%", "%%")
        row_id = yield model.MatrixDB.execute("insert into blog_tag (bid, tag) values ({0}, '{1}')".format(bid, escape_string(tag)))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def delete_tags_by_bid(bid):
        row_id = yield model.MatrixDB.execute("delete from blog_tag where bid = {0}".format(bid))
        raise tornado.gen.Return(row_id)
