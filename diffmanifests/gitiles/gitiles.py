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
        self._url = config['gitiles'].get('host', 'localhost').rstrip('/') + ':' + str(config['gitiles'].get('port', 80)) + '/a'
        self._user = config['gitiles'].get('user', '')

    def commit(self, repo, commit):
        response = requests.get(url=self._url + '/plugins/gitiles/%s/+/%s?format=JSON' % (repo, commit),
                                auth=(self._user, self._pass))
        if response.status_code != requests.codes.ok:
            return None
        return json.loads(response.text.replace(")]}'", ''))

    def commits(self, repo, branch, commit):
        response = requests.get(url=self._url + '/plugins/gitiles/%s/+log/%s/?s=%s&format=JSON' % (repo, branch, commit),
                                auth=(self._user, self._pass))
        if response.status_code != requests.codes.ok:
            return None
        return json.loads(response.text.replace(")]}'", ''))
