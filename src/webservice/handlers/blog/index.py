# coding=utf-8

from handlers.base import BaseController
from tornado.web import gen

from model.blog.blog import Blog
from model.user import User
from model.blog.read import Read
from model.blog.praise import Praise
from model.blog.comment import Comment

class BlogIndexHandler(BaseController):

    item_in_page = 20

    @gen.coroutine
    def get(self):
        page = self.get_argument('page', '')
        search = self.get_argument('search', '')

        if search != "":
            pass
        else:
            if page == "": page = "1"

        blogs = yield Blog.get_blog_list(str(int(page) - 1), self.item_in_page)

        for blog in blogs:
            blog.author = yield User.get_user_by_id(blog.author)
            blog.reads = yield Read.get_read_num_by_bid(blog.bid)
            blog.praises = yield Praise.get_praise_num_by_bid(blog.bid)
            blog.comments = yield Comment.get_comment_num_by_bid(blog.bid)

        blogs_count = yield Blog.get_blog_num()

        top_blogs = yield self.get_top_blogs_by_count(5)

        data = {
            'current_user' : self.current_user,
            'page_current' : page,
            'page_count' : blogs_count / self.item_in_page + 1,
            'blogs' : blogs,
            'top_blogs' : top_blogs
        }

        self.render('blog/index.jade', **data)

    @gen.coroutine
    def get_top_blogs_by_count(self, count):
        top_blogs = yield Blog.get_top_blogs_by_count(count)

        for blog in top_blogs:
            blog.author = yield User.get_user_by_id(blog.author)

        raise gen.Return(top_blogs)
