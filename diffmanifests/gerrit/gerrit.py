# -*- coding: utf-8 -*-

import json
import requests


class GerritException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Gerrit(object):
    def __init__(self, config):
        if config is None:
            raise GerritException('Invalid gerrit config')
        self._pass = config['gerrit'].get('pass', '')
        self._query = config['gerrit'].get('query', {'option': ['CURRENT_REVISION']})
        self._user = config['gerrit'].get('user', '')
        self._url = config['gerrit'].get('url', 'localhost:80')
        if len(self._pass) != 0 and len(self._user) != 0:
            self._url += '/a'

    def get(self, _id):
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.get(url=self._url+'/changes/'+str(_id)+'/detail', auth=(self._user, self._pass))
        else:
            response = requests.get(url=self._url+'/changes/'+str(_id)+'/detail')
        if response.status_code != requests.codes.ok:
            return None
        return json.loads(response.text.replace(")]}'", ''))

    def query(self, search, start):
        payload = {
            'o': self._query['option'],
            'q': search,
            'start': start
        }
        if len(self._pass) != 0 and len(self._user) != 0:
            response = requests.get(url=self._url+'/changes/', auth=(self._user, self._pass), params=payload)
        else:
            response = requests.get(url=self._url+'/changes/', params=payload)
        if response.status_code != requests.codes.ok:
            return None
        return json.loads(response.text.replace(")]}'", ''))

    def url(self):
        return self._url
