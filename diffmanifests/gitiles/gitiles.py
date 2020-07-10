# -*- coding: utf-8 -*-

import json
import requests


class GitilesException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Gitiles(object):
    def __init__(self, config=None):
        if config is None or config.get('gitiles', None) is None:
            raise GitilesException('config invalid')
        self._pass = config['gitiles'].get('pass', '')
        self._url = config['gitiles'].get('url', 'http://localhost:80').rstrip('/')
        self._user = config['gitiles'].get('user', '')

    def commit(self, repo, commit):
        if len(self._pass) == 0 or len(self._user) == 0:
            response = requests.get(url=self._url + '/%s/+/%s?format=JSON' % (repo, commit))
        else:
            response = requests.get(url=self._url + '/%s/+/%s?format=JSON' % (repo, commit),
                                    auth=(self._user, self._pass))
        if response.status_code != requests.codes.ok:
            return None
        return json.loads(response.text.replace(")]}'", ''))

    def commits(self, repo, branch, commit):
        if len(self._pass) == 0 or len(self._user) == 0:
            response = requests.get(url=self._url + '/%s/+log/%s/?s=%s&format=JSON' % (repo, branch, commit))
        else:
            response = requests.get(url=self._url + '/%s/+log/%s/?s=%s&format=JSON' % (repo, branch, commit),
                                    auth=(self._user, self._pass))
        if response.status_code != requests.codes.ok:
            return None
        return json.loads(response.text.replace(")]}'", ''))

    def url(self):
        return self._url
