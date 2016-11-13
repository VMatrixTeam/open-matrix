from handlers.base import BaseController
from tornado.web import gen

from model.snippet.snippet import Snippet
from model.snippet.praise import Praise
from model.snippet.comment import Comment
from model.user import User

import json

class SnippetIndexHandler(BaseController):

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

    @gen.coroutine
    def get_top_snippets_by_count(self, count):
        top_snippets = yield Snippet.get_top_snippets_by_count(count)

        for snippet in top_snippets:
            snippet.author = yield User.get_user_by_id(snippet.author)
            snippet.praises = yield Praise.get_praises_by_sid(snippet.sid)
            snippet.comments = yield Comment.get_comments_by_sid(snippet.sid)
            snippet.pictures = json.loads(snippet.pictures)
            snippet.is_praised = False
            for each in snippet.praises:
                if each.user_id == self.current_user.user_id:
                    snippet.is_praised = True
                    break
        raise gen.Return(top_snippets)

    @gen.coroutine
    def get(self):
        page = self.get_argument('page', '')
        search = self.get_argument('search', '')

        if search != '':
            # deal with search
            pass

        else:
            if page == '': page = 1
            snippets, snippets_count = yield self.get_snippets_by_page(page)

        top_snippets = yield self.get_top_snippets_by_count(5)

        data = {
            "current_user": self.current_user,
            "snippets" : sorted(snippets, self.cpm_snippet),
            "top_snippets" : top_snippets
        }

        self.render('snippet/snippet.jade', **data)

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
