
import model
import tornado.gen

from MySQLdb import escape_string

import random

class Score(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_user_score(user_id):
        result = yield model.MatrixDB.get(
            """
                select sum(score) as score from question_score where user_id = {0}
            """.format(
                user_id
            )
        )
        raise tornado.gen.Return(result.score)

    @staticmethod
    @tornado.gen.coroutine
    def get_rank_list():
        result = yield model.MatrixDB.query(
            """
                select user_id, sum(score) as score from question_score group by user_id order by score desc limit 0,10
            """
        )
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def add_score(socre, reason, user_id):

        socre = int((random.random() + 0.5) * socre)

        yield model.MatrixDB.execute(
            """
                insert into question_score (user_id, score, reason) values ({0}, {1}, '{2}')
            """.format(user_id, socre, escape_string(reason))
        )
