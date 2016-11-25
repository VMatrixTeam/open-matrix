# coding=utf-8

from handlers.base import BaseController
from tornado import gen

from model.blog.blog import Blog
from model.blog.tag import Tag

import datetime

import json

class BlogHandler(BaseController):
    @gen.coroutine
    def check_blog(self, content, title, tags):
        if content == "" or title == "":
            self.sendError("缺少参数"); raise gen.Return(False)

        if len(title) > 50:
            self.sendError("title 参数过长"); raise gen.Return(False)

        if len(content) > 10000:
            self.sendError("content 参数过长"); raise gen.Return(False)

        # print('json.loads(tags)')
        # print(json.loads(tags))
        try:
            tags = json.loads(tags)
            if type(tags) != list:
                raise Exception;
        except:
            self.sendError("参数错误"); raise gen.Return(False)

        if len(tags) > 5:
            self.sendError("tag 参数过长"); raise gen.Return(False)

        for tag in tags:
            if len(tag) > 10:
                self.sendError("tag 中的参数过长"); raise gen.Return(False)

        raise gen.Return(True)

    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == "create":
            content = self.get_argument('content', '')
            title = self.get_argument('title', '')
            tags = self.get_argument('tags', '')

            check = yield self.check_blog(content, title, tags)

            if not check:
                raise gen.Return()

            user_blogs = yield Blog.get_blogs_by_uid_latest_100(self.current_user.user_id)

            # if sum(1 for blog in user_blogs if blog.createAt > datetime.datetime.today() - datetime.timedelta(hours=1)) > 0:
            #     self.sendError("Sorry! alpha 1.0 版本规定每小时限制创建1个blog"); raise gen.Return()

            bid = yield Blog.create_blog(self.current_user.user_id, title, '', content)

            # Score.add_score(50, "create question "+str(e_question.qid), self.current_user.user_id)

            tags = json.loads(tags)

            for tag in tags:
                tid = yield Tag.create_tag(bid, tag)

            self.sendData(True, "创建成功", {'bid' : bid})

        elif method == "delete":
            pass
            # qid = self.get_argument("qid", "")
            # if qid == "" or not qid.isdigit():
            #     self.sendError("qid 参数错误"); raise gen.Return()

            # e_question = yield Question.get_question_by_qid(qid)

            # if not e_question:
            #     self.sendError("不存在的qid"); raise gen.Return()

            # if e_question.author != self.current_user.user_id:
            #     self.sendError("没有权限操作"); raise gen.Return()

            # yield Question.delete_question_by_qid(qid)

            # Score.add_score(-50, "delete question "+str(e_question.qid), self.current_user.user_id)

            # self.sendData(True, "操作成功")

        elif method == "update":
            pass
            # qid = self.get_argument('qid', '')
            # description = self.get_argument('description', '')
            # title = self.get_argument('title', '')
            # tags = self.get_argument('tags', '')

            # check = yield self.check_question(description, title, tags)

            # if not check:
            #     raise gen.Return()

            # e_question = yield Question.get_question_by_qid(qid)

            # if not e_question:
            #     self.sendError("查无此qid"); raise gen.Return()
            # print e_question.author

            # if e_question.author != self.current_user.user_id:
            #     self.sendError("没有权限"); raise gen.Return()

            # Question.update_question(qid, description, title)

            # yield Tag.delete_tags_by_qid(qid)

            # tags = json.loads(tags)

            # for tag in tags:
            #     yield Tag.create_tag(qid, tag)

            # self.sendData(True, "操作成功", {'qid' : qid}); raise gen.Return()

        else:
            self.sendError("未知操作"); raise gen.Return()
