#coding:utf-8

from tornado.web import RequestHandler
from handlers.base import BaseController
from tornado import gen

from model.files import File
from model.user import User

import os
import config


class MatrixAvatarHandler(RequestHandler):
    avatar_file_path = os.path.join(config.get_config()["service"]["file-system"]["root_path"], "data", "avatar")

    @gen.coroutine
    def get(self, user_id):

        user = yield User.get_user_by_id(user_id)

        if user == None:
            self.finish({
                'result' : False,
                'msg' : '没有该用户',
                'data' : None
            })
            raise gen.Return()

        if os.path.exists(os.path.join(self.avatar_file_path, user.avatar)):
            with open(os.path.join(self.avatar_file_path, user.avatar), 'rb') as avatar:
                self.set_header ('Content-Type', 'application/octet-stream')
                self.set_header ('Content-Disposition', 'attachment; filename='+user.avatar)
                self.finish(avatar.read())
        else:
            self.redirect(self.static_url("images/default-avatar.jpg"))

    def post(self):
        pass


class PictureUploadHandler(BaseController):
    cache_path = os.path.join(config.get_config()["service"]["file-system"]["root_path"], "data", "upload")

    @gen.coroutine
    def get(self, filename):
        if not os.path.exists(os.path.join(self.cache_path, filename)):
            self.sendError("文件不存在")
            raise gen.Return()
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename=' + filename)
        self.finish(file(os.path.join(self.cache_path, filename), 'rb').read())

    @gen.coroutine
    def post(self, blank):
        file_metas = self.request.files["file"]

        if len(file_metas) > 1:
            self.sendError("每次只能上传一个图片")
            raise gen.Return()
        file_meta = file_metas[0]
        content_type = file_meta['content_type']
        filename = file_meta['filename']
        # check_file_exist
        if os.path.exists(os.path.join(self.cache_path, filename)):
            self.sendError("文件重名")
            raise gen.Return()

        file_name = str(int(time.time() * 1000000)) + filename

        if len(file_meta['body']) > 700000:
            self.sendError("文件太大")
            raise gen.Return()

        user_record = yield File.get_user_file_record(self.current_user.user_id)

        print sum(1 for each in user_record if each.uploadAt > datetime.datetime.today() - datetime.timedelta(hours=1))

        if user_record and sum(1 for each in user_record if each.uploadAt > datetime.datetime.today() - datetime.timedelta(hours=1)) > 30:
            self.sendError("用户接口限制")
            raise gen.Return()

        yield File.create_record(file_name, self.current_user.user_id)

        with open(os.path.join(self.cache_path, file_name), 'wb+') as fb:
            fb.write(file_meta['body'])

        url = config.get_config()['runtime']['protocol'] + "://"+config.get_config()['runtime']["base-url"]
        if config.ENV == 'development':
            url += ":" + str(config.get_config()['runtime']['port'])
        url += "/"

        url += '/api/1.0/base/filesystem/picture/' + file_name

        self.finish({
            'result' : False,
            'msg' : '上传成功',
            'filename' : url,
        })

class SnippetPictureUploadHandler(BaseController):
    cache_path = os.path.join(config.get_config()["service"]["file-system"]["root_path"], "data", "upload", "snippet")

    @gen.coroutine
    def get(self, filename):
        if not os.path.exists(os.path.join(self.cache_path, filename)):
            self.finish({
                'result' : False,
                'msg' : '文件不存在',
                'filename' : None
            })
            raise gen.Return()
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename=' + filename)
        self.finish(file(os.path.join(self.cache_path, filename), 'rb').read())
