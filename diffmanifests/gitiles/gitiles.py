# -*- coding: utf-8 -*-

import json
import requests

from requests.adapters import HTTPAdapter


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
        self._retry = config['gitiles'].get('retry', 0)
        self._retry = self._retry if self._retry >= 0 else 0
        self._timeout = config['gitiles'].get('timeout', -1)
        self._timeout = self._timeout if self._timeout >= 0 else None
        self._url = config['gitiles'].get('url', 'http://localhost:80').rstrip('/')
        self._user = config['gitiles'].get('user', '')

    def commit(self, repo, commit):
        session = requests.Session()
        session.keep_alive = False
        session.mount('http://', HTTPAdapter(max_retries=self._retry))
        session.mount('https://', HTTPAdapter(max_retries=self._retry))
        if len(self._pass) == 0 or len(self._user) == 0:
            response = session.get(url=self._url + '/%s/+/%s?format=JSON' % (repo, commit), timeout=self._timeout)
        else:
            response = session.get(url=self._url + '/%s/+/%s?format=JSON' % (repo, commit),
                                   auth=(self._user, self._pass), timeout=self._timeout)
        session.close()
        if response.status_code != requests.codes.ok:
            return None
        ret = json.loads(response.text.replace(")]}'", ''))
        return ret

    def commits(self, repo, branch, commit):
        session = requests.Session()
        session.keep_alive = False
        session.mount('http://', HTTPAdapter(max_retries=self._retry))
        session.mount('https://', HTTPAdapter(max_retries=self._retry))
        if len(self._pass) == 0 or len(self._user) == 0:
            response = session.get(url=self._url + '/%s/+log/%s/?s=%s&format=JSON' % (repo, branch, commit),
                                   timeout=self._timeout)
        else:
            response = session.get(url=self._url + '/%s/+log/%s/?s=%s&format=JSON' % (repo, branch, commit),
                                   auth=(self._user, self._pass), timeout=self._timeout)
        session.close()
        if response.status_code != requests.codes.ok:
            return None
        ret = json.loads(response.text.replace(")]}'", ''))
        return ret

    def url(self):
        return self._url
