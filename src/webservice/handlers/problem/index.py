from handlers.base import BaseController
from tornado.web import gen
from model.user import User
from model.problem.problem import Problem

class ProblemIndexHandler(BaseController):
    @gen.coroutine
    def get(self):
        pro_list = yield self.get_problem_list()
        top_pros = yield self.get_top_problems()
        r_users = yield self.get_ranks()

        print pro_list

        data = {
            "current_user" : self.current_user,
            "title" : "Problems",
            "problem_list": pro_list,
            "public_problems": top_pros,
            "rank_users": r_users
        }

        self.render("problem/problem-list.jade", **data)

    @gen.coroutine
    def get_problem_list(self):
      pro_list = yield Problem.get_problem_list()
      for item in pro_list:
          if item['submit_sum'] == 0:
              item['acceptance'] = str(0)+'%'
          else:
              acc = (float(item['passes']) / float(item['submit_sum']))
              item['acceptance'] = str(round(acc, 2)) + '%'
      raise gen.Return(pro_list)

    @gen.coroutine
    def get_top_problems(self):
      top_pros = yield Problem.get_top_problems()
      raise gen.Return(top_pros)

    @gen.coroutine
    def get_ranks(self):
      ranks = yield User.get_rank_users()
      raise gen.Return(ranks)
