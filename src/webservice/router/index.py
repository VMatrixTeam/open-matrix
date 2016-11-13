from handlers.index import login
from handlers.index import logout

from handlers.index import home

urls = [
    (r'/login', login.LoginHandler),
    (r'/login/search', login.UserSearch),
    (r'/logout', logout.LogoutHandler)
]

urls += [
    (r'/', home.LogoutHandler)
]
