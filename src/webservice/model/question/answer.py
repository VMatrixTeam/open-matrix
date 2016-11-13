
import model.base
import tornado.gen
from MySQLdb import escape_string

class Answer(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_answers_by_qid(qid):
        result = yield model.MatrixDB.query("select * from question_answer where qid = {0}".format(qid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_answer_by_aid(aid):
        result = yield model.MatrixDB.get("select * from question_answer where aid = {0}".format(aid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_answers_count_by_qid(qid):
        result = yield model.MatrixDB.get("select count(*) as count from question_answer where qid = {0}".format(qid))
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def create_answer(answer, qid, user_id):
        answer = answer.replace("%", "%%")
        row_id = yield model.MatrixDB.execute("insert into question_answer (qid, description, author, createAt, updateAt) values ({0}, '{1}', {2}, now(), now())".format(qid, escape_string(answer), user_id))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def delete_answer_by_aid(aid):
        row_id = yield model.MatrixDB.execute("delete from question_answer where aid = {0}".format(aid))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def update_answer(aid, content):
        content = content.replace("%", "%%")
        result = yield model.MatrixDB.execute("update question_answer set description = '{0}', updateAt = now() where aid = {1}".format(escape_string(content), aid))
        raise tornado.gen.Return(result)
