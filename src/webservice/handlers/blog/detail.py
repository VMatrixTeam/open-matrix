from handlers.base import BaseController
from tornado.web import gen

from model.blog.blog import Blog
from model.blog.read import Read
from model.blog.praise import Praise
from model.blog.comment import Comment
from model.blog.tag import Tag

from model.user import User

class BlogDetailHandler(BaseController):
    @gen.coroutine
    def get(self, bid):
        blog = yield Blog.get_blog_by_bid(bid)
        if blog == None:
            self.redirect("/404")
            raise gen.Return()

        blog.author = yield User.get_user_by_id(blog.author)
        blog.reads_num = yield Read.get_read_num_by_bid(blog.bid)
        blog.praises_num = yield Praise.get_praise_num_by_bid(blog.bid)
        blog.comments_num = yield Comment.get_comment_num_by_bid(blog.bid)
        blog.comments = yield Comment.get_comments_by_bid(blog.bid)
        blog.tags = yield Tag.get_tags_by_bid(blog.bid)

        author_other_blogs = yield Blog.get_author_other_blogs_by_uid(blog.author.user_id, bid)
        related_blogs = yield Blog.get_related_blogs_by_bid(bid)

        data = {
            "current_user": self.current_user,
            'blog': blog,
            'author_other_blogs': author_other_blogs,
            'related_blogs': related_blogs
        }

        self.render('blog/detail.jade', **data)

        yield Read.create_read(bid, self.current_user.user_id)

    def post(self):
        pass
