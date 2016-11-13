from handlers.base import BaseController
from tornado.web import gen

class ProblemIndexHandler(BaseController):
    @gen.coroutine
    def get(self):
        data = {
            "current_user" : self.current_user,
            "title" : "Problems"
        }

        self.render("problem/problem-list.jade", **data)
