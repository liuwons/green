# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web

from config import *
from wechat_sdk.messages import *


class WX(tornado.web.RequestHandler):
    def wx_proc_msg(self, body):
        try:
            wechat.parse_data(body)
        except ParseError:
            print 'Invalid Body Text'
            return
        id = wechat.message.id          # MsgId
        target = wechat.message.target  # ToUserName
        source = wechat.message.source  # FromUserName
        time = wechat.message.time      # CreateTime
        type = wechat.message.type      # MsgType
        raw = wechat.message.raw        # raw text
        if isinstance(wechat.message, TextMessage):
            content = wechat.message.content
        if isinstance(wechat.message, ImageMessage):
            picurl = wechat.message.picurl                     # PicUrl
            media_id = wechat.message.media_id                 # MediaId
        if isinstance(wechat.message, VoiceMessage):
            media_id = wechat.message.media_id                 # MediaId
            format = wechat.message.format                     # Format
            recognition = wechat.message.recognition           # Recognition
        if isinstance(wechat.message, VideoMessage) or isinstance(wechat.message, ShortVideoMessage):
            media_id = wechat.message.media_id                 # MediaId
            thumb_media_id = wechat.message.thumb_media_id     # ThumbMediaId
        if isinstance(wechat.message, LocationMessage):
            location = wechat.message.location                 # Tuple(X, Y)，(Location_X, Location_Y)
            scale = wechat.message.scale                       # Scale
            label = wechat.message.label                       # Label
        if isinstance(wechat.message, LinkMessage):
            title = wechat.message.title                       # Title
            description = wechat.message.description           # Description
            url = wechat.message.url                           # Url
        if isinstance(wechat.message, EventMessage):
            if wechat.message.type == 'subscribe':  # subscribe
                key = wechat.message.key                        # EventKey
                ticket = wechat.message.ticket                  # Ticket
                return wechat.response_text(content=u'欢迎订阅', escape=True)
            elif wechat.message.type == 'unsubscribe':  # unsubscribe
                return wechat.response_text(content=u'拜拜', escape=True)
            elif wechat.message.type == 'scan':  # scan
                key = wechat.message.key                        # EventKey
                ticket = wechat.message.ticket                  # Ticket
            elif wechat.message.type == 'location':  # location
                latitude = wechat.message.latitude              # Latitude
                longitude = wechat.message.longitude            # Longitude
                precision = wechat.message.precision            # Precision
            elif wechat.message.type == 'click':  # menu click
                key = wechat.message.key                        # EventKey
            elif wechat.message.type == 'view':  # menu link view
                key = wechat.message.key                        # EventKey
            elif wechat.message.type == 'templatesendjobfinish':  # template
                status = wechat.message.status                  # Status
            elif wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto', 'pic_photo_or_album', 'pic_weixin', 'location_select']:  # others
                key = wechat.message.key                        # EventKey
        return wechat.response_text(content=u'知道了', escape=True)

    def get(self):
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        echostr = self.get_argument('echostr', 'default')
        if signature != 'default' and timestamp != 'default' and nonce != 'default' and echostr != 'default' \
                and wechat.check_signature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('Not Open')

    def post(self):
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        if signature != 'default' and timestamp != 'default' and nonce != 'default' \
                and wechat.check_signature(signature, timestamp, nonce):
            body = self.request.body.decode('utf-8')
            try:
                self.write(self.wx_proc_msg(body))
            except IOError, e:
                return
