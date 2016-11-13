from handlers.base import BaseController
from tornado.web import gen

from model.snippet.snippet import Snippet
from model.snippet.praise import Praise
from model.snippet.comment import Comment
from model.user import User

import json

class SnippetCommentHandler(BaseController):

    @gen.coroutine
    def get(self, sid):
        snippet = yield Snippet.get_snippet_by_sid(sid)
        if snippet == None:
            self.finish("404 not found!")
            raise gen.Return()

        snippet.author = yield User.get_user_by_id(snippet.author)
        snippet.praises = yield Praise.get_praises_by_sid(snippet.sid)
        snippet.comments = yield Comment.get_comments_by_sid(snippet.sid)
        snippet.pictures = json.loads(snippet.pictures)
        snippet.is_praised = False
        for each in snippet.praises:
            if each.user_id == self.current_user.user_id:
                snippet.is_praised = True
                break
        snippet.comments = sorted(snippet.comments, self.cpm_comments)
                
        data = {
            "current_user": self.current_user,
            'snippet': snippet
        }

        self.render('snippet/snippet-comment.jade', **data)

    def post(self):
        pass

    @staticmethod
    def cpm_comments(comment_x, comment_y):
        latest_x = comment_x.createAt
        latest_y = comment_y.createAt
        return int((latest_y - latest_x).total_seconds())
