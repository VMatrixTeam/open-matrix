from handlers.base import BaseController
from tornado.web import gen
from tornado.web import authenticated

from model.question.question import Question
from model.question.answer import Answer
from model.question.vote import Vote
from model.user import User
from model.question.tag import Tag
from model.question.score import Score

from operator import itemgetter, attrgetter

class QuestionIndexHandler(BaseController):

    item_in_page = 20

    @gen.coroutine
    def get_questions_detail(self, tab, page):
        if tab == 'hotest':
            questions = yield Question.get_hotest_questions(page * self.item_in_page, self.item_in_page)
        elif tab == "zero-answer":
            questions = yield Question.get_0answer_questions(page * self.item_in_page, self.item_in_page)
        else:
            questions = yield Question.get_newest_questions(page * self.item_in_page, self.item_in_page)


        for question in questions:
            question.author = yield User.get_user_by_id(question.author)
            question.votes = yield Vote.get_votes_count_by_qid(question.qid)
            question.answers = yield Answer.get_answers_by_qid(question.qid)
            question.tags = yield Tag.get_tags_by_qid(question.qid)

        questions_count = yield Question.get_question_count()

        raise gen.Return((questions, questions_count))

    @gen.coroutine
    def get_question_by_search(words):
        words = words.strip().split(" ")

    @gen.coroutine
    def get(self):
        page = self.get_argument('page', '')
        search = self.get_argument('search', '')
        tab = self.get_argument('tab', '')

        if search != '':
            # deal with search
            pass

        else:
            if page == '': page = 1
            questions, questions_count = yield self.get_questions_detail(tab, int(page) - 1)

        rank_list = yield Score.get_rank_list()

        for each in rank_list:
            each.user = yield User.get_user_by_id(each.user_id)

        my_score = yield Score.get_user_score(self.current_user.user_id)

        data = {
            "current_user": self.current_user,
            "title" : "Questions",
            "questions" : questions,
            "page_count": questions_count / self.item_in_page + 1,
            "page_current": page,
            "rank" : rank_list,
            "tab" : tab,
            "my_score" : my_score
        }

        self.render('question/question-list.jade', **data)

    @authenticated
    def post(self):
        pass
