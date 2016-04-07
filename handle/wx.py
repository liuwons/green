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
import hashlib
import urllib
import os
import random
import requests

def check_wx_request(signature, timestamp, nonce):
    token = config.settings['wx_token']
    arr = [token, timestamp, nonce]
    arr.sort()
    sh = hashlib.sha1(arr[0] + arr[1] + arr[2]).hexdigest()
    if sh == signature:
        return True
    else:
        return False

class WX(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        echostr = self.get_argument('echostr', 'default')
        if signature != 'default' and timestamp != 'default' and nonce != 'default' and echostr != 'default' and check_wx_request(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('Not Open')

    def post(self):
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        if signature != 'default' and timestamp != 'default' and nonce != 'default' and check_wx_request(signature, timestamp, nonce):
            body = self.request.body
            try:
                self.write(wx_proc_msg(body))
            except IOError, e:
                return
