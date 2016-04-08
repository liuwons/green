# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web

from BaseHTTPServer import HTTPServer
import base64
import sys
import json
import time

import config
import time


class Index(tornado.web.RequestHandler):
    def get(self):
        self.redirect("http://blog.lwons.com")

    def post(self):
        req = tornado.escape.json_decode(self.request.body)
        self.write("lwons")
