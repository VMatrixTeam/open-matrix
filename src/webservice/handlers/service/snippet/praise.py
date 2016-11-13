# coding=utf-8

from handlers.base import BaseController
from tornado import gen
from model.snippet.praise import Praise

import datetime

import json

class PraiseHandler(BaseController):
    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == "create":
            sid = self.get_argument('sid', '')

            # check = yield self.check_snippet(content)

            # if not check:
            #     raise gen.Return()

            # user_questions = yield      Question.get_questions_by_uid_latest_100(self.current_user.user_id)

            # if sum(1 for question in user_questions if question.createAt > datetime.datetime.today() - datetime.timedelta(hours=1)) > 0:
            #     self.finish({
            #         'result' : False,
            #         'msg' : "Sorry! alpha 1.0 版本规定每小时限制创建1个问题",
            #         'data' : None
            #     })
            #     raise gen.Return()

            is_praised = True if (yield Praise.get_praises_count_by_sid_user_id(sid, self.current_user.user_id)) else False
            if is_praised:
                self.finish({
                    'result' : False,
                    'msg' : "Sorry! 你已经赞过了!",
                    'data' : None
                })
                raise gen.Return()

            pid = yield Praise.create_praise(sid, self.current_user.user_id)

            # tags = json.loads(tags)

            # for tag in tags:
            #     tid = yield Tag.create_tag(qid, tag)

            self.finish({
                'result' : True,
                'msg' : "创建成功",
                'data' : {
                    'pid' : pid
                }
            })
        else:
            pass