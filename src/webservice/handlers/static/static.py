from handlers.base import BaseController

class StaticHandler(BaseController):
    def get(self, page):
        if page == "about":
            self.render("static/about.jade")
            return 
        self.render("static/construction.jade")
