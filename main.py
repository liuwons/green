import tornado.web
import tornado.httpserver
from tornado.options import define, options

import config

define("port", default=config.settings['port'], help="run on the given port", type=int)

if __name__ == '__main__':
    app = tornado.web.Application(config.web_handlers, **config.settings)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

