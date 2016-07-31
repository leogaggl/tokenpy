import requests
import datetime
import pytz
import simplejson as json
from ConfigParser import SafeConfigParser

class RemoteDataStore(object):

    def __init__(self):
        config = SafeConfigParser()
        config.read("tokenpy.cfg")
        self.app_id = config.get('Buddy Config', 'app_id')
        self.app_key = config.get('Buddy Config', 'app_key')
        self.app_url = config.get('Buddy Config', 'app_url')
        self.app_url = config.get('Buddy Config', 'app_url')
        self.app_name = config.get('Buddy Config', 'app_name')
        self.access_token = ""
        self.service_root = config.get('Buddy Config', 'app_url')
        
    def get_access_token(self):
        payload = {'appid': self.app_id, 'appkey': self.app_key, 'platform': 'REST Client'}
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        resp = requests.request('POST', self.app_url + '/devices', params=payload, headers=headers, timeout=5)
        
        if (resp.ok):
            result =json.loads(resp.content)
            for r in result['result']:
                if 'accessToken' in r:
                    self.access_token = result['result']['accessToken']
                if 'serviceRoot' in r:
                    self.service_root = result['result']['serviceRoot']
        else:
            print(resp.text)
        
    def configure_telemetry(self):
        payload = json.dumps({'uniqueIdKey': 'sid', 'metrics': {'sid': 'sid', 'movement': 'movement', 'temperature': 'temperature', 'humidity': 'humidity', 'battery': 'battery'}})
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Buddy ' + self.access_token}
        resp = requests.request('put', self.service_root + '/telemetry/' + self.app_name, params=payload, headers=headers, timeout=5)
        
        if (resp.ok):
            result = json.loads(resp.content)
        else:
            print(resp.content)
            print("Error configuring telemetry")
        
    def add_telemetry_data(self, measurement, fields, source_info):
        payload = json.dumps({'data': fields, 'location': '-34.92295629, 138.59124184'})
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Buddy ' + self.access_token}
        resp = requests.request('post', self.service_root + '/telemetry/' + self.app_name, data=payload, headers=headers, timeout=5)
        
        if (resp.ok):
            result = json.loads(resp.content)
            print(result)
        else:
            print(payload)
            print(resp.content)
            print("Error adding telemetry")