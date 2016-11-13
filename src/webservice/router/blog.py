from handlers.blog.index import BlogIndexHandler
from handlers.blog.detail import BlogDetailHandler

urls = [
    (r'/blog', BlogIndexHandler),
    (r'/blog/detail/(.*)', BlogDetailHandler)
]
