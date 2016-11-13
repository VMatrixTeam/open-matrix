from handlers.base import BaseController
from tornado.web import gen

class BlogDetailHandler(BaseController):
    @gen.coroutine
    def get(self, bid):
        page = self.get_argument('page', '')
        search = self.get_argument('search', '')

        if search != '':
            # deal with search
            pass

        self.render('blog/detail.jade')
