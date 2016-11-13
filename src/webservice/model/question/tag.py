
import model.base
import tornado.gen

from MySQLdb import escape_string

class Tag(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_tags_by_qid(qid):
        result = yield model.MatrixDB.query("select * from question_tag where qid = {0} limit 0, 5".format(qid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_tags_like_name(name):
        result = yield model.MatrixDB.query("select tag, count(*) as count from question_tag where tag like '%%{0}%%'group by tag order by count desc limit 0, 5".format(escape_string(name)))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def create_tag(qid, tag):
        tag = tag.replace("%", "%%")
        row_id = yield model.MatrixDB.execute("insert into question_tag (qid, tag) values ({0}, '{1}')".format(qid, escape_string(tag)))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def delete_tags_by_qid(qid):
        row_id = yield model.MatrixDB.execute("delete from question_tag where qid = {0}".format(qid))
        raise tornado.gen.Return(row_id)
