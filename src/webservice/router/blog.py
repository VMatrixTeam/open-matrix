from handlers.blog.index import BlogIndexHandler
from handlers.blog.detail import BlogDetailHandler
from handlers.blog.edit import BlogCreateHandler

urls = [
    (r'/blog', BlogIndexHandler),
    (r'/blog/detail/(.*)', BlogDetailHandler),
    (r'/blog/create', BlogCreateHandler)
]
