from handlers.static.static import StaticHandler

from tornado.web import StaticFileHandler

urls = [
    (r'/static-page/(.*)', StaticHandler),
    (r'/(favicon.ico)', StaticFileHandler, r"static/favicon.ico")
]
