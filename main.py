import tornado.web
import tornado.httpserver
from tornado.options import define, options

from config import *

define("port", default=80, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
	app = Application()
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
    
