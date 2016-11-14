import model.base
import tornado.gen

from MySQLdb import escape_string

class User(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_user_by_id(user_id):
        result = yield model.MatrixDB.get("select * from user where user_id = {0}".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_uid_by_username_or_email(username_email):
        result = yield model.MatrixDB.query("select user_id from user where username='{0}' or email = '{0}'".format(escape_string(username_email)))
        if len(result) == 0:
            raise tornado.gen.Return(None)
        else:
            raise tornado.gen.Return(result[0])

    @staticmethod
    @tornado.gen.coroutine
    def get_heat_datetimes_by_user_id(user_id):
        result = yield model.MatrixDB.query("\
            select createAt from question_answer where author = '{0}' \
            union \
            select createAt from question_comment where author = '{0}' \
            union \
            select createAt from question_question where author = '{0}' \
            order by createAt ASC".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_question_records_by_user_id(user_id):
        result = yield model.MatrixDB.query("\
            SELECT qid, title, description, createAt \
            FROM question_question \
            where author = '{0}' \
            order by createAt ASC".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_answer_records_by_user_id(user_id):
        result = yield model.MatrixDB.query("\
            SELECT aid, qid, description, createAt \
            FROM question_answer \
            where author = '{0}' \
            order by createAt ASC".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_oldest_comment_record_by_user_id(user_id):
        result = yield model.MatrixDB.query("\
            SELECT cid, aid, qid, description, createAt \
            FROM question_comment \
            where author = '{0}' \
            order by createAt ASC limit 0,1".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_rank_users():
        result = yield model.MatrixDB.query("\
            SELECT u.user_id, SUM(s.grade) as grade \
            from user u, submission s \
            where s.user_id = u.user_id \
            GROUP BY s.user_id \
            order by grade desc \
            limit 0, 10")
        raise tornado.gen.Return(result)
