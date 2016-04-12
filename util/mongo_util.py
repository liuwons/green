import pymongo
import randid
import datetime


class MongoUtil:
    def __init__(self, db_ip='localhost', db_name='wx'):
        self.db_ip = db_ip
        self.db_name = db_name
        self.db_user_collection = 'user'
        self.db_host_collection = 'host'
        self.db_cmmd_collection = 'cmmd'

        self.client = pymongo.MongoClient(db_ip, 27017)
        self.db = self.client[db_name]
        self.user_collection = self.db[self.db_user_collection]
        self.host_collection = self.db[self.db_host_collection]
        self.cmmd_collection = self.db[self.db_cmmd_collection]

    def __del__(self):
        self.client.close()

    @staticmethod
    def make_id(openid):
        return randid.randid(4) + openid[-4:]

    def upsert_user(self, openid):
        user = {'openid': openid, 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.user_collection.update({'openid': openid}, user, upsert=True)

    def delete_user(self, openid):
        self.user_collection.remove({'openid': openid})
        self.host_collection.remove({'openid': openid})
        self.cmmd_collection.remove({'openid': openid})

    def query_user(self, openid):
        users = self.user_collection.find({'openid': openid})
        if users.count() == 0:
            return None
        else:
            return users[0]

    def host_count(self, openid):
        return self.host_collection.find({'openid': openid}).count()

    def insert_host(self, openid):
        host = {'id': self.make_id(openid)+openid[-4:], 'openid': openid, 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.host_collection.insert(host)
        return host['id']

    def query_hosts(self, openid):
        hosts = self.host_collection.find({'openid': openid})
        if hosts.count() == 0:
            return None
        else:
            results = []
            for host in hosts:
                results.append(host)
            return results

