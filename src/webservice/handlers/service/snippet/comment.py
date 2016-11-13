# coding=utf-8

from handlers.base import BaseController
from tornado import gen
from model.snippet.comment import Comment

import datetime

import json

class CommentHandler(BaseController):

    @gen.coroutine
    def check_length(self, content, length):
        if content == '':
            self.finish({
                'result' : False,
                'msg' : "缺少参数",
                'data' : None
            })
            raise gen.Return(False)

        if len(content) > length:
            self.finish({
                'result' : False,
                'msg' : "content 参数过长",
                'data' : None
            })
            raise gen.Return(False)

        raise gen.Return(True)

    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == "create":
            content = self.get_argument('content', '')
            sid = self.get_argument('sid', '')

            check = yield self.check_length(content, 148)

            if not check:
                raise gen.Return()

            # user_questions = yield      Question.get_questions_by_uid_latest_100(self.current_user.user_id)

            # if sum(1 for question in user_questions if question.createAt > datetime.datetime.today() - datetime.timedelta(hours=1)) > 0:
            #     self.finish({
            #         'result' : False,
            #         'msg' : "Sorry! alpha 1.0 版本规定每小时限制创建1个问题",
            #         'data' : None
            #     })
            #     raise gen.Return()

            cid = yield Comment.create_comment(content, sid, self.current_user.user_id)

            # tags = json.loads(tags)

            # for tag in tags:
            #     tid = yield Tag.create_tag(qid, tag)

            self.finish({
                'result' : True,
                'msg' : "创建成功",
                'data' : {
                    'cid' : cid
                }
            })
        else:
            pass