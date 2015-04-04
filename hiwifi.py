# coding: utf-8
import re
import requests
import netifaces


class Hiwifi:
    def __init__(self):
        self.session = requests.session()
        self.ip = netifaces.gateways()['default'].popitem()[1][0]
        self.base_url = 'http://' + self.ip + '/cgi-bin/turbo/'

    def login(self, password):
        response = self.session.post(self.base_url + 'admin_web', {
            'username': 'admin',
            'password': password,
        })
        match = re.search(u'已经错误.*次', response.text)
        if match:
            return match.group()
        else:
            self.stok = re.search('stok=\w+', response.text).group()
            self.api_base_url = self.base_url + ';' + self.stok + '/api/'
            return True

    def get(self, api):
        return self.session.get(self.api_base_url + api).json()

    def devices(self):
        return self.get('network/device_list')

    def traffics(self):
        return self.get('qos/get_traffic_list')

if __name__ == '__main__':
    hiwifi = Hiwifi()
    hiwifi.login('2099420')
    print(hiwifi.devices())
