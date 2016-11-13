from handlers.snippet.index import SnippetIndexHandler
from handlers.snippet.comment import SnippetCommentHandler

urls = [
    (r'/snippet', SnippetIndexHandler),
    (r'/snippet/comment/(.*)', SnippetCommentHandler)
]
