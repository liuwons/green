# -*- coding: utf-8 -*-
import os
import tornado.web

settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'template_path': os.path.join(os.path.dirname(__file__), 'view'),
            'cookie_secret':'e440769943b4e8442f09de341f3fea28462d2341f483a0ed9a3d5d3859f==78d',
            'login_url':'/',
            'session_secret':"3cdcb1f07693b6e75ab50b466a40b9977db123440c28307f428b25e2231f1bcc",
            'session_timeout':3600,

            'wx_token': 'weixin',

            'host_name': 'a.lwons.com',
            }

from handle import *

handlers=[
        (r'/', common.Index),
        (r'/wx', wx.WX),

        #static resource route
        (r"/(favicon\.ico)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
        ]
