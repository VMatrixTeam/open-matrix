# coding=utf-8

from handlers.base import BaseController
from tornado import gen
from model.question.answer import Answer
from model.question.question import Question
from model.question.score import Score

class AnswerHandler(BaseController):
    @gen.coroutine
    def get(self):
        pass

    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == "create":
            answer = self.get_argument('answer', '')
            question = self.get_argument('question', '')

            if answer == "":
                self.sendError("缺少 answer 参数")
                raise gen.Return()

            if len(answer) > 3000:
                self.sendError("参数过长"); raise gen.Return()

            if question == "":
                self.sendError("缺少 question 参数"); raise gen.Return()

            e_question = yield Question.get_question_by_qid(question)

            if e_question == None:
                self.sendError("question 不存在"); raise gen.Return()

            aid = yield Answer.create_answer(answer, question, self.current_user.user_id)

            Score.add_score(20, "answer question "+str(e_question.qid), self.current_user.user_id)

            self.sendData(True, "创建成功", {'aid' : aid})

        elif method == "delete":
            aid = self.get_argument("aid", "")

            if aid == "" or not aid.isdigit():
                self.sendError("aid 参数错误"); raise gen.Return()

            e_answer = yield Answer.get_answer_by_aid(aid)

            if not e_answer:
                self.sendError("不存在的aid"); raise gen.Return()

            if e_answer.author != self.current_user.user_id:
                self.sendError("没有权限操作"); raise gen.Return()

            yield Answer.delete_answer_by_aid(aid)
            Score.add_score(-20, "delete answer "+str(e_answer.aid), self.current_user.user_id)

            self.sendData(True, "操作成功", aid)

        elif method == "update":
            aid = self.get_argument('aid', '')
            content = self.get_argument('content', '')

            if aid == '' or not aid.isdigit():
                self.sendError("aid参数错误"); raise gen.Return()

            if content == '' or len(content) > 3000:
                self.sendError("content长度不符合"); raise gen.Return()

            result = yield Answer.update_answer(aid, content)

            self.sendData(True, "操作成功")

        else:
            self.sendError("未知操作"); raise gen.Return()
