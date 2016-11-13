
import model.base
import tornado.gen

from MySQLdb import escape_string

class Comment(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_comment_by_cid(cid):
        result = yield model.MatrixDB.get("select * from question_comment where cid = {0}".format(cid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_comments_by_qid(qid):

        result = yield model.MatrixDB.query("select * from question_comment where qid = {0}".format(qid))

        for each in result:
            each.author = yield model.MatrixDB.get("select * from user where user_id = {0}".format(each.author))

        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_comments_by_aid(aid):
        result = yield model.MatrixDB.query("select * from question_comment where aid = {0}".format(aid))
        for each in result:
            each.author = yield model.MatrixDB.get("select * from user where user_id = {0}".format(each.author))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def create_question_comment(comment, qid, user_id):
        comment = comment.replace("%", "%%")
        row_id = yield model.MatrixDB.execute("insert into question_comment (qid, aid, description, author, createAt, updateAt) values ({0}, -1, '{1}', {2}, now(), now())".format(qid, escape_string(comment), user_id))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def create_answer_comment(comment, aid, user_id):
        comment = comment.replace("%", "%%")
        row_id = yield model.MatrixDB.execute("insert into question_comment (qid, aid, description, author, createAt, updateAt) values (-1, {0}, '{1}', {2}, now(), now())".format(aid, escape_string(comment), user_id))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def delete_comment_by_cid(cid):
        row_id = yield model.MatrixDB.execute("delete from question_comment where cid = {0}".format(cid))
        raise tornado.gen.Return(row_id)
