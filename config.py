# -*- coding: utf-8 -*-
import os
import json
import tornado.web

from wechat_sdk.core.conf import WechatConf
from wechat_sdk.basic import WechatBasic

settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'template_path': os.path.join(os.path.dirname(__file__), 'view'),
            'cookie_secret': 'e440769943b4e8442f09de341f3fea28462d2341f483a0ed9a3d5d3859f==78d',
            'login_url': '/',
            'session_secret': "3cdcb1f07693b6e75ab50b466a40b9977db123440c28307f428b25e2231f1bcc",
            'session_timeout': 3600,

            'port': 5601,
            'wx_token': 'weixin',
            }

wx_token = None
wx_appid = None
wx_secrert = None
wx_mode = None

with open("conf.json") as f:
    conf_str = f.read()
    js = json.loads(conf_str)
    wx_token = js['token']
    wx_appid = js['appid']
    wx_secrert = js['secret']
    wx_mode = js['mode']

wx_conf = WechatConf(token=wx_token, appid=wx_appid, appsecret=wx_secrert, encrypt_mode=wx_mode)
wechat = WechatBasic(conf=wx_conf)

with open("menu.json") as f:
    menu_str = f.read()
    js = json.loads(menu_str)
    wechat.delete_menu()
    wechat.create_menu(js)


from handle import *

handlers=[
        (r'/', common.Index),
        (r'/wx', wx.WX),

        (r"/(favicon\.ico)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
        (r"/(.*\.html)", tornado.web.StaticFileHandler, {"path": "static/"}),
        ]
