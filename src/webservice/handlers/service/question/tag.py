# coding=utf-8

from handlers.base import BaseController
from tornado import gen

from model.question.tag import Tag

class TagHandler(BaseController):
    @gen.coroutine
    def get(self):
        pass

    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == '':
            self.sendError("缺少method参数"); raise gen.Return()

        if method == 'search':
            query = self.get_argument('query', '')
            if query == "":
                self.sendData(True, "操作成功", []); raise gen.Return()

            result = yield Tag.get_tags_like_name(query)

            self.sendData(True, "操作成功", [tag.tag for tag in result]); raise gen.Return()

        else:
            self.sendError("不支持的方法")
            raise gen.Return()
