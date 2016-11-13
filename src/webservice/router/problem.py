
from handlers.problem.index import ProblemIndexHandler
from handlers.problem.detail import ProblemDetailHandler

urls = [
    (r"/problem", ProblemIndexHandler),
    (r"/problem/detail/(.*)", ProblemDetailHandler)
]
