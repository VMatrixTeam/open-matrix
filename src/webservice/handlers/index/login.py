# coding=utf-8

from tornado import gen
from tornado.web import RequestHandler
from model.user import User

import md5

class LoginHandler(RequestHandler):
    def get(self):
        self.render('index/login.jade')

    @gen.coroutine
    def post(self):
        username_email = self.get_argument('username_email', '')
        password = self.get_argument('password', '')

        if username_email == "" or password == "":
            self.finish({
                'result': False,
                'msg' : '用户名或者密码不能为空'
            })
            raise gen.Return()

        user_find = yield User.get_uid_by_username_or_email(username_email)

        if user_find == None:
            self.finish({
                'result' : False,
                'msg' : '用户不存在',
                'data' : None
            })
            raise gen.Return()

        user = yield User.get_user_by_id(user_find.user_id)
        userSalt = 'matrix-is-the-best-system-in-the-world'
        password = md5.new(password + userSalt).hexdigest()

        if password == user.password:
            self.set_secure_cookie('matrix', str(user.user_id));
            self.finish({
                'result' : True,
                'msg' : '验证成功',
                'data' : None
            })
        else:
            self.finish({
                'result' : False,
                'msg' : '密码错误',
                'data' : None
            })


class UserSearch(RequestHandler):
    @gen.coroutine
    def get(self):
        username_email = self.get_argument('username_email', '')
        if username_email == "":
            self.finish({
                'result' : False,
                'msg' : 'user not found',
                'data' : None
            })
            raise gen.Return()
        user_find = yield User.get_uid_by_username_or_email(username_email)

        if user_find == None:
            self.finish({
                'result' : False,
                'msg' : 'user not found',
                'data' : None
            })
        else:
            self.finish({
                'result' : True,
                'msg' : '',
                'data' : user_find.user_id
            })
