#coding:utf-8

import router

urls = []

urls += router.question.urls
urls += router.snippet.urls
urls += router.blog.urls

urls += router.index.urls
urls += router.static.urls
urls += router.api.urls
urls += router.user.urls
urls += router.problem.urls

from handlers.index.error import ExceptionHandler

urls += [(r".*", ExceptionHandler)]
