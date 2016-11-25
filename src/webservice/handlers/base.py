
# json module
import json
import model

# tornado web module
import tornado.web
from tornado import template
from tornado import gen

# logging module
import logging
logger = logging.getLogger('matrix-console.' + __name__)

# pyjade template engine
from pyjade.ext.tornado import patch_tornado
patch_tornado()

from model.user import User

class BaseController(tornado.web.RequestHandler):

    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def sendData(self, result=False, msg="", data=None):
        self.write({
            "result" : result,
            "msg" : msg,
            "data" : data
        })

    def sendError(self, msg=""):
        self.sendData(msg=msg)

    def get_all_arguments_list(self):
        arguments = self.request.arguments
        ret = {}
        for argument in arguments.items():
            for each in argument[1]:
                ret[argument[0]] = each
        return ret

    @classmethod
    def logged(self, func):
        def with_logging(*args, **kwargs):
            if self.get_secure_cookie('matrix'):
                return func(*args, **kwargs)
            else:
                self.redirect("/login")
        return with_logging

    @gen.coroutine
    def prepare(self):
        if self.get_secure_cookie("matrix"):
            user_id = self.get_secure_cookie("matrix")
            self.current_user = yield User.get_user_by_id(user_id)
            raise gen.Return(self.current_user)
        else:
            self.redirect('/login')
            raise gen.Return(None)

    def permission(func):
        """Access control generator
        """
        print "permission"
        return func

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.
        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg
