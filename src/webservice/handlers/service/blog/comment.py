# coding=utf-8

from handlers.base import BaseController
from tornado import gen
from model.blog.comment import Comment
from model.blog.blog import Blog

class CommentHandler(BaseController):
    @gen.coroutine
    def get(self):
        pass

    @gen.coroutine
    def post(self):
        method = self.get_argument('method', '')

        if method == "create":
            content = self.get_argument('content', '')
            bid = self.get_argument('bid', '')

            if content == "":
                self.sendError("缺少 content 参数"); raise gen.Return()

            if len(content) > 3000:
                self.sendError("content 参数过长"); raise gen.Return()

            if bid == "":
                self.sendError("缺少 bid 参数"); raise gen.Return()

            e_blog = yield Blog.get_blog_by_bid(bid)
            if e_blog == None:
                self.sendError("blog 不存在"); raise gen.Return()
            cid = yield Comment.create_comment(self.current_user.user_id, bid, content)

            self.sendData(True, "创建成功", {"bid" : bid})

        elif method == "delete":
            pass
            # cid = self.get_argument("cid", "")
            # if cid == "" or not cid.isdigit():
            #     self.sendError("错误的参数: cid"); raise gen.Return()

            # e_comment = yield Comment.get_comment_by_cid(cid)

            # if not e_comment:
            #     self.sendError("comment不存在"); raise gen.Return()

            # if e_comment.author != self.current_user.user_id:
            #     self.sendError("没有权限"); raise gen.Return()

            # Comment.delete_comment_by_cid(e_comment.cid)
            # Score.add_score(-10, "delete comment "+str(e_comment.cid), self.current_user.user_id)

            # self.sendData(True, "操作成功", e_comment.cid)

        else:
            self.sendError("未知操作"); raise gen.Return()
