from handlers.service.question.answer import AnswerHandler
from handlers.service.question.comment import CommentHandler
from handlers.service.question.vote import VoteHandler
from handlers.service.question.tag import TagHandler
from handlers.service.question.question import QuestionHandler

from handlers.service.blog.blog import BlogHandler
from handlers.service.blog.praise import PraiseHandler as BlogPraiseHandler

from handlers.service.snippet.snippet import SnippetHandler
from handlers.service.snippet.praise import PraiseHandler as SnippetPraiseHandler
from handlers.service.snippet.comment import CommentHandler as SnippetCommentHandler

from handlers.service.user.contribution import ContributionHandler

from handlers.service.base import filesystem

version = "1.0"

urls = [
    (r'/api/{0}/question/answer'.format(version), AnswerHandler),
    (r'/api/{0}/question/comment'.format(version), CommentHandler),
    (r'/api/{0}/question/vote'.format(version), VoteHandler),
    (r'/api/{0}/question/tag'.format(version), TagHandler),
    (r'/api/{0}/question/question'.format(version), QuestionHandler),
    
    (r'/api/{0}/blog/blog'.format(version), BlogHandler),
    (r'/api/{0}/blog/praise'.format(version), BlogPraiseHandler),

    (r'/api/{0}/snippet/snippet'.format(version), SnippetHandler),
    (r'/api/{0}/snippet/praise'.format(version), SnippetPraiseHandler),
    (r'/api/{0}/snippet/comment'.format(version), SnippetCommentHandler),

    (r'/api/{0}/profile/contribution'.format(version), ContributionHandler),

    (r'/api/{0}/base/filesystem/avatar/(.*)'.format(version), filesystem.MatrixAvatarHandler),
    (r'/api/{0}/base/filesystem/picture/(.*)'.format(version), filesystem.PictureUploadHandler),
    (r'/api/{0}/base/filesystem/picture/snippet/(.*)'.format(version), filesystem.SnippetPictureUploadHandler)
]
