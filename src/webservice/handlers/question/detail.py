# coding=utf-8

from handlers.base import BaseController

from tornado.web import gen

from model.question.question import Question
from model.question.answer import Answer
from model.question.vote import Vote
from model.user import User
from model.question.tag import Tag
from model.question.comment import Comment

class QuestionDetailHandler(BaseController):
    @gen.coroutine
    def get(self, qid):
        question = yield Question.get_question_by_qid(qid)
        if question == None:
            self.redirect("/404")
            raise gen.Return()

        question.author = yield User.get_user_by_id(question.author)
        question.votes = yield Vote.get_votes_by_qid(question.qid)
        question.answers = yield Answer.get_answers_count_by_qid(question.qid)
        question.tags = yield Tag.get_tags_by_qid(question.qid)
        question.comments = yield Comment.get_comments_by_qid(question.qid)

        answers = yield Answer.get_answers_by_qid(question.qid)

        for answer in answers:
            answer.author = yield User.get_user_by_id(answer.author)
            answer.comments = yield Comment.get_comments_by_aid(answer.aid)
            answer.votes = yield Vote.get_votes_by_aid(answer.aid)

        data = {
            "current_user": self.current_user,
            'question': question,
            'answers' : answers
        }

        self.render('question/question-detail.jade', **data)

    def post(self):
        pass
