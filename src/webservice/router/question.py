from handlers.question.index import QuestionIndexHandler
from handlers.question.detail import QuestionDetailHandler
from handlers.question.edit import QuestionCreateHandler
from handlers.question.edit import QuestionModifyHandler
from handlers.question.edit import AnswerCreateHandler
from handlers.question.edit import AnswerModifyHandler

urls = [
    (r'/question', QuestionIndexHandler),
    (r'/question/index', QuestionIndexHandler),
    (r'/question/detail/(.*)', QuestionDetailHandler),
    (r'/question/create', QuestionCreateHandler),
    (r'/question/edit/(.*)', QuestionModifyHandler),
    (r'/question/answer/create/(.*)', AnswerCreateHandler),
    (r'/question/answer/edit/(.*)', AnswerModifyHandler)
]
