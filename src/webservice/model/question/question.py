
import model
import tornado.gen

from MySQLdb import escape_string

class Question(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_newest_questions(id_from, count):
        result = yield model.MatrixDB.query(
            """
                SELECT
                  *
                FROM
                  (
                  SELECT
                    question.qid,
                    question.description,
                    question.author,
                    question.title,
                    question.createAt,
                    question.updateAt,
                    CASE WHEN answer.time IS NULL THEN question.updateAt WHEN question.updateAt > answer.time THEN question.updateAt ELSE answer.time
                END AS TIME
                FROM
                  question_question AS question
                LEFT JOIN
                  (
                  SELECT
                    qid,
                    MAX(updateAt) AS TIME
                  FROM
                    question_answer
                  GROUP BY
                    qid
                ) AS answer
                ON
                  question.qid = answer.qid
                ) AS result
                ORDER BY
                  result.time
                DESC
                LIMIT {0}, {1}
            """.format(
                id_from,
                count
            )
        )
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_hotest_questions(id_from, count):
        result = yield model.MatrixDB.query(
            """
                SELECT
                  *
                FROM
                  question_question AS question
                LEFT JOIN
                  (
                  SELECT
                    qid as rqid,
                    COUNT(*) AS hot
                  FROM
                    question_answer
                  GROUP BY
                    rqid
                ) AS answer
                ON
                  answer.rqid = question.qid
                ORDER BY
                  answer.hot
                DESC
                LIMIT
                    {0}, {1}
            """.format(id_from, count)
        )
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_0answer_questions(id_from, count):
        result = yield model.MatrixDB.query(
            """
                SELECT
                  *
                FROM
                  question_question AS question
                LEFT JOIN
                  (
                  SELECT
                    qid as rqid ,
                    COUNT(*) AS hot
                  FROM
                    question_answer
                  GROUP BY
                    rqid
                ) AS answer
                ON
                  answer.rqid = question.qid
                WHERE
                  answer.hot IS NULL
                ORDER BY
                  question.updateAt
                DESC
                LIMIT
                    {0}, {1}
            """.format(id_from, count)
        )
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_questions(id_from, count):
        result = yield model.MatrixDB.query("select * from question_question limit {0}, {1}".format(id_from, count))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_questions_by_uid_latest_100(user_id):
        result = yield model.MatrixDB.query("select * from question_question where author = {0} order by createAt desc limit 0, 100".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def create_question(description, title, user_id):
        description = description.replace("%", "%%")
        row_id = yield model.MatrixDB.execute("insert into question_question (author, title, description, createAt, updateAt) values ({0}, '{1}', '{2}', now(), now())".format(user_id, escape_string(title), escape_string(description)))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def get_question_by_qid(qid):
        result = yield model.MatrixDB.get("select * from question_question where qid = {0}".format(qid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_question_count():
        result = yield model.MatrixDB.get("select count(*) as count from question_question")
        raise tornado.gen.Return(result.count)

    @staticmethod
    @tornado.gen.coroutine
    def delete_question_by_qid(qid):
        result = yield model.MatrixDB.execute("delete from question_question where qid = {0}".format(qid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def update_question(qid, description, title):
        description = description.replace("%", "%%")
        result = model.MatrixDB.execute("update question_question set description = '{0}', title = '{1}', updateAt = now() where qid = {2}".format(
            escape_string(description),
            escape_string(title),
            qid
        ))
        raise tornado.gen.Return(result)
