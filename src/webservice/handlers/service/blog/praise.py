# coding=utf-8

from handlers.base import BaseController
from tornado import gen

from model.blog.praise import Praise

import datetime

import json

class PraiseHandler(BaseController):
    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == "create":
            bid = self.get_argument('bid', '')

            is_praised = True if (yield Praise.get_praises_count_by_bid_user_id(bid, self.current_user.user_id)) else False
            if is_praised:
                self.finish({
                    'result' : False,
                    'msg' : "Sorry! 你已经赞过了!",
                    'data' : None
                })
                raise gen.Return()

            pid = yield Praise.create_praise(bid, self.current_user.user_id)

            self.finish({
                'result' : True,
                'msg' : "点赞成功",
                'data' : {
                    'pid' : pid
                }
            })
        else:
            pass