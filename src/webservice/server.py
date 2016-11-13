#coding:utf-8

import config
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def init_tornado(ENVIRONMENT):
    """
    this function is use to init tornado web server, notice that this function must be executed at last
    """

    config.set_config(ENVIRONMENT)

    CONFIG = config.get_config()

    import tornado.ioloop
    import tornado.web
    import tornado.httpserver
    import tornado.options

    from urls import urls

    # application

    SETTINGS = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=CONFIG['runtime']['debug'],
        login_url="/login",
        cookie_secret=CONFIG['runtime']['cookie-secret']
    )

    application = tornado.web.Application(
        handlers = urls,
        **SETTINGS
    )

    print 'Development server is running at {0}://{1}:{2}/'.format(
        CONFIG['runtime']['protocol'],
        CONFIG['runtime']['base-url'],
        CONFIG['runtime']['port']
    )

    print 'Quit the server with CONTROL-C'

    for each in urls:
        print each[0],'\t',each[1] # print urls

    if ENVIRONMENT != "production":
        tornado.options.parse_command_line()
        server = tornado.httpserver.HTTPServer(application)
        server.listen(CONFIG['runtime']['port'])
        tornado.ioloop.IOLoop.instance().start()
    else:
        # mutiple processes in production environment
        server = tornado.httpserver.HTTPServer(application)
        server.bind(CONFIG['runtime']['port'])
        server.start(0)  # forks one process per cpu
        tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':

    Environment = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ["development", "production", "testing"] else "development"

    init_tornado(Environment)
