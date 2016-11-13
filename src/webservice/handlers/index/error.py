from handlers.base import BaseController

class ExceptionHandler(BaseController):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('static/error.jade', code='404', message="404 not found!")
        elif status_code == 500:
            self.render('static/error.jade', code='500', message="internal server error 500!")
        else:
            self.render('static/error.jade', code=str(status_code), message="Error " + str(status_code))
