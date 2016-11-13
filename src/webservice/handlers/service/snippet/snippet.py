# coding=utf-8

from handlers.base import BaseController
from tornado import gen
from model.snippet.snippet import Snippet
from model.snippet.praise import Praise
from model.snippet.comment import Comment
from model.user import User

import tornado

import datetime

import json

from model.files import File

import os
import time

import config

import re

class SnippetHandler(BaseController):

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
    def check_code_length(self, content, length):
        if len(content) > length:
            self.finish({
                'result' : False,
                'msg' : "code 参数过长",
                'data' : None
            })
            raise gen.Return(False)

        raise gen.Return(True)

    @gen.coroutine
    def post(self):
        # deal with content
        content = self.get_argument('content', '')

        check = yield self.check_length(content, 148)

        if not check:
            raise gen.Return()

        # deal with code
        code = self.get_argument('code', '')

        check = yield self.check_code_length(code, 2000)

        if not check:
            raise gen.Return()

        # deal with pictures
        pictures = []
        if self.request.files:
            file_metas = self.request.files["images"]
            # if len(file_metas) > 1:
            #     self.finish({
            #         'result' : False,
            #         'msg' : '每次只能上传一个图片',
            #         'filename' : None
            #     })
            #     raise gen.Return()
            for i in range(len(file_metas)):
                file_meta = file_metas[i]
                content_type = file_meta['content_type']
                filename = file_meta['filename']

                # check_file_type
                if not re.search('^image/', content_type, re.I):
                    self.finish({
                        'result' : False,
                        'msg' : '图片格式错误',
                        'filename' : None
                    })
                    raise gen.Return()

                # check_file_exist
                if os.path.exists(os.path.join(self.cache_path, filename)):
                    self.finish({
                        'result' : False,
                        'msg' : '文件重名',
                        'filename' : None
                    })
                    raise gen.Return()

                # check_file_size
                if len(file_meta['body']) > 700000:
                    self.finish({
                        'result' : False,
                        'msg' : '文件太大',
                        'filename' : None
                    })
                    raise gen.Return()

                # 用户接口检查
                # user_record = yield File.get_user_file_record(self.current_user.user_id)

                # print sum(1 for each in user_record if each.uploadAt > datetime.datetime.today() - datetime.timedelta(hours=1))

                # if user_record and sum(1 for each in user_record if each.uploadAt > datetime.datetime.today() - datetime.timedelta(hours=1)) > 30:
                #     self.finish({
                #         'result' : False,
                #         'msg' : '用户接口限制',
                #         'filename' : None
                #     })
                #     raise gen.Return()

                file_name = str(int(time.time() * 1000000)) + filename

                # yield File.create_record(file_name, self.current_user.user_id)

                with open(os.path.join(self.cache_path, file_name), 'wb+') as fb:
                    fb.write(file_meta['body'])

                pictures.append(file_name)

                # url = config.get_config()['runtime']['protocol'] + "://"+config.get_config()['runtime']["base-url"]
                # if config.ENV == 'development':
                #     url += ":" + str(config.get_config()['runtime']['port'])
                # url += "/"

                # url += 'service.base/filesystem/picture/' + file_name

        user_snippets = yield      Snippet.get_snippets_by_uid_latest_count(self.current_user.user_id, 10)

        if sum(1 for snippet in user_snippets if snippet.createAt > datetime.datetime.today() - datetime.timedelta(minutes=10)) >= 2:
            self.finish({
                'result' : False,
                'msg' : "Sorry! alpha 1.0 版本规定每10分钟限制创建2个Snippet",
                'data' : None
            })
            raise gen.Return()

        sid = yield Snippet.create_snippet(content, code, pictures, self.current_user.user_id)

        self.finish({
            'result' : True,
            'msg' : "创建成功",
            'data' : {
                'sid' : sid
            }
        })

        # # 只提交content的处理
        # if method == "create":
        #     content = self.get_argument('content', '')

        #     check = yield self.check_snippet(content)

        #     if not check:
        #         raise gen.Return()

        #     # user_questions = yield      Question.get_questions_by_uid_latest_100(self.current_user.user_id)

        #     # if sum(1 for question in user_questions if question.createAt > datetime.datetime.today() - datetime.timedelta(hours=1)) > 0:
        #     #     self.finish({
        #     #         'result' : False,
        #     #         'msg' : "Sorry! alpha 1.0 版本规定每小时限制创建1个问题",
        #     #         'data' : None
        #     #     })
        #     #     raise gen.Return()

        #     sid = yield Snippet.create_snippet(content, self.current_user.user_id)

        #     # tags = json.loads(tags)

        #     # for tag in tags:
        #     #     tid = yield Tag.create_tag(qid, tag)

        #     self.finish({
        #         'result' : True,
        #         'msg' : "创建成功",
        #         'data' : {
        #             'sid' : sid
        #         }
        #     })
        # else:
        #     pass

    @gen.coroutine
    def get(self):

        page = self.get_argument('page', '')

        if page == '' or page < 1:
            raise gen.Return()

        snippets, snippets_count = yield self.get_snippets_by_page(page)

        data = {
            "snippets" : sorted(snippets, self.cpm_snippet)
        }

        self.render('snippet/snippets.jade', **data)

    @gen.coroutine
    def get_snippets_by_page(self, page):
        snippets = yield Snippet.get_snippets((int(page) - 1) * 10, 10)

        for snippet in snippets:
            snippet.author = yield User.get_user_by_id(snippet.author)
            snippet.praises = yield Praise.get_praises_by_sid(snippet.sid)
            snippet.comments = yield Comment.get_comments_by_sid(snippet.sid)
            snippet.pictures = json.loads(snippet.pictures)
            snippet.is_praised = False
            for each in snippet.praises:
                if each.user_id == self.current_user.user_id:
                    snippet.is_praised = True
                    break
        snippets_count = yield Snippet.get_snippet_count()

        raise gen.Return((snippets, snippets_count))

    @staticmethod
    def cpm_snippet(snippet_x, snippet_y):
        latest_x = snippet_x.createAt
        latest_y = snippet_y.createAt
        for comment_x in snippet_x.comments:
            if comment_x.createAt > latest_x:
                latest_x = comment_x.createAt
        for comment_y in snippet_y.comments:
            if comment_y.createAt > latest_y:
                latest_y = comment_y.createAt
        return int((latest_y - latest_x).total_seconds())
