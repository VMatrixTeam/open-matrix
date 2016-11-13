# coding=utf-8

from handlers.base import BaseController
from tornado import gen
from model.question.answer import Answer
from model.question.question import Question
from model.question.comment import Comment
from model.question.score import Score

class CommentHandler(BaseController):
    @gen.coroutine
    def get(self):
        pass

    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == "create":
            comment = self.get_argument('comment', '')
            ctype = self.get_argument('type', '')
            qaid = self.get_argument('qaid', '')

            if comment == "":
                self.sendError("缺少 comment 参数"); raise gen.Return()

            if len(comment) > 400:
                self.sendError("comment 参数过短"); raise gen.Return()

            if ctype == "" or ctype not in ["question", "answer"]:
                self.sendError("缺少 type 参数 或参数错误"); raise gen.Return()

            if qaid == "":
                self.sendError("缺少 qa 参数"); raise gen.Return()

            if ctype == "question":
                e_question = yield Question.get_question_by_qid(qaid)
                if e_question == None:
                    self.sendError("question 不存在"); raise gen.Return()
                cid = yield Comment.create_question_comment(comment, qaid, self.current_user.user_id)


            elif ctype == "answer":
                e_answer = yield Answer.get_answer_by_aid(qaid)
                if e_answer == None:
                    self.sendError("answer 不存在"); raise gen.Return()
                cid = yield Comment.create_answer_comment(comment, qaid, self.current_user.user_id)

            else:

                assert(False)

            self.sendData(True, "创建成功", {"cid" : cid})

        elif method == "delete":
            cid = self.get_argument("cid", "")
            if cid == "" or not cid.isdigit():
                self.sendError("错误的参数: cid"); raise gen.Return()

            e_comment = yield Comment.get_comment_by_cid(cid)

            if not e_comment:
                self.sendError("comment不存在"); raise gen.Return()

            if e_comment.author != self.current_user.user_id:
                self.sendError("没有权限"); raise gen.Return()

            Comment.delete_comment_by_cid(e_comment.cid)
            Score.add_score(-10, "delete comment "+str(e_comment.cid), self.current_user.user_id)

            self.sendData(True, "操作成功", e_comment.cid)

        else:
            self.sendError("未知操作"); raise gen.Return()
