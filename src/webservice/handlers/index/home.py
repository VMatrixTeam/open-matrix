import handlers.base

class LogoutHandler(handlers.base.BaseController):
    def get(self):
        self.render("index/home.jade")

    def post(self):
        pass
