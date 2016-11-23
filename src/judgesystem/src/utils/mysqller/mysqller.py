#_*_coding=utf-8_*_
import MySQLdb

class Mysqller():
    @staticmethod
    def execute(sql, method, **kwargs):
        '''
        将对数据库的操作封装成一个静态的方法，其中method表示要做的操作，update或者query
        kwargs中包括数据库的相关配置信息
        '''
        result = None
        try:
            conn = MySQLdb.connect(**kwargs)
        except:
            return result

        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print 'finished commit'
        except:
            conn.close()
            return result

        if 'query' == method:
            result = cur.fetchall()
        conn.close()
        return result
