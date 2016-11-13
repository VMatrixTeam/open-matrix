from handlers.base import BaseController
from tornado.web import gen


class ProblemDetailHandler(BaseController):
    @gen.coroutine
    def get(self, pid):
        data = {
            "current_user" : self.current_user,
            "title" : "Problems"
        }

        self.render("problem/problem-detail.jade", **data)
