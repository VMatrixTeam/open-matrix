from handlers.base import BaseController
from tornado.web import gen

class BlogCreateHandler(BaseController):
    def get(self):
        data = {
            'title' : 'Write A Blog',
            'blog' : None
        }
        self.render('blog/edit.jade', **data)

    def post(self):
        pass
