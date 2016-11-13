# coding=utf-8

from handlers.base import BaseController
from tornado import gen
from model.question.answer import Answer
from model.question.question import Question
from model.question.comment import Comment
from model.question.vote import Vote
from model.question.score import Score

class VoteHandler(BaseController):
    @gen.coroutine
    def get(self):
        pass

    @gen.coroutine
    def post(self):
        value = self.get_argument("value", "")
        vtype = self.get_argument("type", "")
        qaid = self.get_argument("qaid", "")

        if value not in ["0", "1"] or vtype not in ["answer", "question"] or not qaid.isdigit():
            self.sendError("缺少参数"); raise gen.Return()

        if vtype == "question":
            e_question = yield Question.get_question_by_qid(qaid)
            if e_question == None:
                self.sendError("qaid 错误"); raise gen.Return()

            if e_question.author == self.current_user.user_id:
                self.sendError("不能给自己投票"); raise gen.Return()

            voted = yield Vote.get_vote_by_qid_uid(qaid, self.current_user.user_id)

            if len(voted) != 0 :
                self.sendError("已经投票过了"); raise gen.Return()

            Vote.create_question_vote(qaid, value, self.current_user.user_id)

            Score.add_score(50 * (-1 if value == "0" else 1), "voted by "+str(self.current_user.nickname), e_question.author)

        elif vtype == "answer":
            e_answer = yield Answer.get_answer_by_aid(qaid)
            if e_answer == None:
                self.sendError("qaid 错误"); raise gen.Return()

            if e_answer.author == self.current_user.user_id:
                self.sendError("不能给自己投票"); raise gen.Return()

            voted = yield Vote.get_vote_by_aid_uid(qaid, self.current_user.user_id)

            if len(voted) != 0 :
                self.sendError("已经投票过了"); raise gen.Return()

            Vote.create_answer_vote(qaid, value, self.current_user.user_id)

            Score.add_score(50 * (-1 if value == "0" else 1), "voted by "+str(self.current_user.nickname), e_answer.author)

        else:
            assert(False)

        self.sendData(True, '投票成功')
