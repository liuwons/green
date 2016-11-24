# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web
import csv
import DBProcess


from config import *
from wechat_sdk.messages import *


class WX(tornado.web.RequestHandler):
    def wx_proc_msg(self, body):
        try:
            wechat.parse_data(body)
        except ParseError:
            print '[ERROR] Parse message failed.'
            return
        id = wechat.message.id          # MsgId
        target = wechat.message.target  # ToUserName
        source = wechat.message.source  # FromUserName
        time = wechat.message.time      # CreateTime
        type = wechat.message.type      # MsgType
        raw = wechat.message.raw        # raw text
        if isinstance(wechat.message, TextMessage):
            content = wechat.message.content
            if len(content.replace(' ', '')) == 0:
                return wechat.response_none()
            li = content.lower().encode('utf-8').split()
            print(li)
            if li[0] == 'borrow':
                if len(li) == 1:
                    DBResult = []
                    with open('list.csv', 'rb') as csvfile:
    		            reader = csv.reader(csvfile, delimiter=' ')
    		            for row in reader:
                            print row
    			            if row[1] == '0':
    				            DBResult.append(row)
    			            elif row[1] == '1':
    				            DBResult.append(row)
    			            elif row[1] == '*':
    				            DBResult.append(row)
    			            else:
    				            return wechat.response_text(content="list.csv error")#list.csv error,the status flag must be 1, 0 or *


    	            returnString = ''
                    for i in range(len(DBResult)):
                        if DBList[i][1] == '1':
                            returnString += DBResult[i][2]
    			            returnString += ' Available\n'
                        elif DBList[i][1] == '0':
    			            returnString += DBResult[i][2]
    			            returnString += ' Unavailable\n'
    		            else:
    			            returnString += '***'
    			            returnString += DBResult[i][2]
    			            returnString += '***\n'
                    return wechat.response_text(content=returnString.decode('utf-8'))
                elif len(li) == 2:
                    text = DBProcess.borrowEquipment(li[1])
                    if text == 2:
                        return wechat.response_text(content="list.csv error")
                    return wechat.response_text(content=text)
                else:
                    return wechat.response_text(content="Wrong Command!")
            if  li[0] == 'return':
                if len(li) == 2:
                    text = DBProcess.returnEquipment(li[1])
                    if text == 2:
                        return wechat.response_text(content="list.csv error")
                    return wechat.response_text(content=text)
                else:
                    return wechat.response_text(content="Wrong Command!")
            return wechat.response_text(content="Wrong Command!")
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
                mongo.upsert_user(source)
                return wechat.response_text(content=u'''欢迎关注''')
            elif wechat.message.type == 'unsubscribe':  # unsubscribe
                mongo.delete_user(source)
                return None
            elif wechat.message.type == 'scan':  # scan
                key = wechat.message.key                        # EventKey
                ticket = wechat.message.ticket                  # Ticket
            elif wechat.message.type == 'location':  # location
                latitude = wechat.message.latitude              # Latitude
                longitude = wechat.message.longitude            # Longitude
                precision = wechat.message.precision            # Precision
            elif wechat.message.type == 'click':  # menu click
                key = wechat.message.key                       # EventKey
                if key == 'HOST_ADD':
                    host_count = mongo.host_count(source)
                    if host_count >= max_host_count:
                        return wechat.response_text(content=u'添加主机失败，已达到最大主机数目')
                    host_id = mongo.insert_host(source)
                    return wechat.response_text(content=u'添加主机成功，主机ID：' + host_id)
                elif key == 'HOST_DELETE':
                    hosts = mongo.query_hosts(source)
                    if hosts is None or len(hosts) == 0:
                        return wechat.response_text(content=u'您还尚未添加任何主机')
                    resp = u'选择需要删除的主机:\n'
                    for i in range(len(hosts)):
                        resp += u'''<a href="http://lwons.com/fw/host_delete?id=%s">%s</a>\n''' % (hosts[i]['id'], hosts[i]['id'])
                    return wechat.response_text(content=resp)
                elif key == 'HOST_STATUS':
                    return wechat.response_text(content=u'''<a href="http://lwons.com/fw/host_status?id=%s">点击查看主机状态</a>''' % source)
                elif key == 'HOST_COMMAND':
                    return wechat.response_text(content=u'''<a href="http://lwons.com/fw/host_cmmd?id=%s">进入命令页</a>''' % source)
                elif key == 'MINE_PROFILE':
                    return wechat.response_text(content=u'个人信息')
                elif key == 'MINE_HOSTS':
                    hosts = mongo.query_hosts(source)
                    if hosts is None or len(hosts) == 0:
                        return wechat.response_text(content=u'您还尚未添加任何主机')
                    resp = u'您的所有主机：\n'
                    for i in range(len(hosts)):
                        resp += u'%s  %s\n' % (hosts[i]['id'], hosts[i]['time'])
                    return wechat.response_text(content=resp)
            elif wechat.message.type == 'view':  # menu link view
                key = wechat.message.key                        # EventKey
                return wechat.response_text(key, escape=True)
            elif wechat.message.type == 'templatesendjobfinish':  # template
                status = wechat.message.status                  # Status
            elif wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto', 'pic_photo_or_album', 'pic_weixin', 'location_select']:  # others
                key = wechat.message.key                        # EventKey
        return wechat.response_text(content=u'知道了')

    def get(self):
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        echostr = self.get_argument('echostr', 'default')
        if signature != 'default' and timestamp != 'default' and nonce != 'default' and echostr != 'default' \
                and wechat.check_signature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('Page Not Available')

    def post(self):
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        # check if the data is sent by WeChat server
        if signature != 'default' and timestamp != 'default' and nonce != 'default' \
                and wechat.check_signature(signature, timestamp, nonce):
            body = self.request.body.decode('utf-8')
            try:
                result = self.wx_proc_msg(body)
                if result is not None:
                    self.write(result)
            except IOError, e:
                return

    def checkDB():
        DBResult = []
        with open('list.csv', 'rb') as csvfile:
    		reader = csv.reader(csvfile, delimiter=' ')
    		for row in reader:
    			if row[1] == '0':
    				DBResult.append(row)
    			elif row[1] == '1':
    				DBResult.append(row)
    			elif row[1] == '*':
    				DBResult.append(row)
    			else:
    				return 2
    	print DBResult
    	return DBResult

    def changeDB(arg, num):	#Caution!!! arg and num are all String!

    	newCSVList = []
    	oldCSVList = checkDB()
    	if oldCSVList == 2:
    		return 2 #list.csv error,the status flag must be 1, 0 or *

    	for i in range(len(oldCSVList)):
    		if oldCSVList[i][0] == num:
    			newRow = oldCSVList[i]
    			newRow[1] = arg
    			newCSVList.append(newRow)
    		else:
    			newCSVList.append(oldCSVList[i])
    	#rewrite the list.csv
    	with open('list.csv', 'wb') as csvfile:
    		writer = csv.writer(csvfile, delimiter=' ')
    		writer.writerows(newCSVList)

    	return 0

    def borrowEquipment(num):#Caution!!! num is a string!
    	DBList = checkDB()
    	if DBList == 2:
    		return 2

    	order = 999 #the order of the equipment in the DBList

    	for i in range(len(DBList)):
    		if DBList[i][0] == num:
    			order = i
    			break

    	if order == 999:
    		return 'The equipment number does not exsist'

    	if DBList[order][1] == '0':
    		return 'The equipment has been lent out.' #if the equipment has been lent out, return this to show the error
    	elif DBList[order][1] == '1':
    		if changeDB('0', num) == 0:
    			return 'Succeed!' # succeed
    	else:
    		return 2 #list.csv error(the status flag must be 1, 0 or *), return 2 to show the error

    def returnEquipment(num):#Caution!!! num is a string!
    	DBList = checkDB()
    	if DBList == 2:
    		return 2 #list.csv error,the status flag must be 1, 0 or *

    	order = 999 #the order of the equipment in the DBList

    	for i in range(len(DBList)):
    		if DBList[i][0] == num:
    			order = i
    			break
    	if order == 999:
    		return 'The equipment number does not exsist'

    	if DBList[order][1] == '1':
    		return 'The equipment hasn\'t been lent out.' #if the equipment has not been lent out, return this to show the error
    	if DBList[order][1] == '0':
    		if changeDB('1', num) == 0:
    			return 'Succeed!' # succeed

    def showEquipment():
        DBResult = []
        with open('list.csv', 'rb') as csvfile:
    		reader = csv.reader(csvfile, delimiter=' ')
    		for row in reader:
    			if row[1] == '0':
    				DBResult.append(row)
    			elif row[1] == '1':
    				DBResult.append(row)
    			elif row[1] == '*':
    				DBResult.append(row)
    			else:
    				DBResult = [2]

    	if DBResult == [2]:
    		return 2 #list.csv error,the status flag must be 1, 0 or *

    	returnString = ''
    	for i in range(len(DBResult)):
    		if DBList[i][1] == '1':
    			returnString += DBResult[i][2]
    			returnString += ' Available\n'
    		elif DBList[i][1] == '0':
    			returnString += DBResult[i][2]
    			returnString += ' Unavailable\n'
    		else:
    			returnString += '***'
    			returnString += DBResult[i][2]
    			returnString += '***\n'
