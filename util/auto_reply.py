# -*- coding: utf-8 -*-
import json
import requests
import traceback


class TulingAutoReply:
    def __init__(self, tuling_key, tuling_url):
        self.key = tuling_key
        self.url = tuling_url

    def reply(self, unicode_str):
        body = {'key': self.key, 'info': unicode_str.encode('utf-8')}
        r = requests.post(self.url, data=body)
        r.encoding = 'utf-8'
        resp = r.text
        if resp is None or len(resp) == 0:
            return None
        try:
            js = json.loads(resp)
            if js['code'] == 100000:
                return js['text'].replace('<br>', '\n')
            elif js['code'] == 200000:
                return js['url']
            else:
                return None
        except Exception:
            traceback.print_exc()
            return None


class DefaultAutoReply:
    def __init__(self):
        pass

    def reply(self, unicode_str):
        return None
