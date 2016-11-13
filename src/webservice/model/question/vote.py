
import model.base
import tornado.gen

class Vote(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_all_votes():
        result = yield model.MatrixDB.query("select * from question_vote")
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_votes_by_qid(qid):
        result = yield model.MatrixDB.query("select * from question_vote where qid = {0}".format(qid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_votes_by_aid(aid):
        result = yield model.MatrixDB.query("select * from question_vote where aid = {0}".format(aid))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_vote_by_qid_uid(qid, user_id):
        result = yield model.MatrixDB.query("select * from question_vote where qid = {0} and voter = {1}".format(qid, user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_vote_by_aid_uid(aid, user_id):
        result = yield model.MatrixDB.query("select * from question_vote where aid = {0} and voter = {1}".format(aid, user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def get_votes_count_by_qid(qid):
        result = yield model.MatrixDB.query("select value from question_vote where qid = {0}".format(qid))
        raise tornado.gen.Return(sum(1 if vote.value else -1 for vote in result))

    @staticmethod
    @tornado.gen.coroutine
    def create_question_vote(qid, value, user_id):
        row_id = yield model.MatrixDB.execute("insert into question_vote (qid, aid, voter, value) values ({0}, -1, {1}, {2})".format(qid, user_id, value))
        raise tornado.gen.Return(row_id)

    @staticmethod
    @tornado.gen.coroutine
    def create_answer_vote(aid, value, user_id):
        row_id = yield model.MatrixDB.execute("insert into question_vote (qid, aid, voter, value) values (-1, {0}, {1}, {2})".format(aid, user_id, value))
        raise tornado.gen.Return(row_id)
