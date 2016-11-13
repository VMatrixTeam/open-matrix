import handlers.base

class LogoutHandler(handlers.base.BaseController):
    def get(self):
        self.clear_cookie('matrix')
        self.redirect('/login')

    def post(self):
        pass
