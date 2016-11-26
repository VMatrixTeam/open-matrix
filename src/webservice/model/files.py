import model
import tornado.gen
from MySQLdb import escape_string

class File(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_user_file_record(user_id):
        result = yield model.MatrixDB.query("select * from file_record where user_id = {0}".format(user_id))
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def create_record(filename, user_id):
        result = yield model.MatrixDB.execute("insert into file_record (filename, user_id, uploadAt) values ('{0}', {1}, now())".format(escape_string(filename), user_id))
        raise tornado.gen.Return(result)
