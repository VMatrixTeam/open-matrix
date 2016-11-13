
from tornado import gen

from handlers.base import BaseController

from model.question.question import Question
from model.question.tag import Tag
from model.question.answer import Answer

class QuestionCreateHandler(BaseController):
    def get(self):
        data = {
            'title' : 'Create Question',
            'question' : None
        }
        self.render('question/question-edit.jade', **data)

    def post(self):
        pass

class QuestionModifyHandler(BaseController):
    @gen.coroutine
    def get(self, qid):

        if qid == "" or not qid.isdigit():
            self.redirect("/404")
            raise gen.Return()

        e_question = yield Question.get_question_by_qid(qid)

        if not e_question:
            self.redirect("/404")
            raise gen.Return()

        e_question.tags = yield Tag.get_tags_by_qid(qid)


        data = {
            'title' : 'Modify Question',
            'question' : e_question
        }

        self.render('question/question-edit.jade', **data)

class AnswerCreateHandler(BaseController):
    @gen.coroutine
    def get(self, qid):

        data = {
            'title' : 'Create Answer',
            'data' :  {
                'qid' : qid
            }
        }

        self.render('question/answer-edit.jade', **data)


class AnswerModifyHandler(BaseController):
    @gen.coroutine
    def get(self, aid):

        if aid == "" or not aid.isdigit():
            self.redirect("/404")
            raise gen.Return()

        e_answer = yield Answer.get_answer_by_aid(aid)

        if not e_answer:
            self.redirect("/404")
            raise gen.Return()

        data = {
            'title' : 'Modify Answer',
            'data' : {
                'answer' : e_answer
            }
        }

        self.render("question/answer-edit.jade", **data)
