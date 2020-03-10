# -*- coding: utf-8 -*-

import os
import pprint
import requests

from diffmanifests.main import load
from diffmanifests.proto.proto import Diff
from diffmanifests.querier.querier import Querier, QuerierException


def test_exception():
    exception = QuerierException('exception')
    assert str(exception) == 'exception'


def test_querier():
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    querier = Querier(config)
    assert querier is not None

    repo = 'platform/build'
    branch = 'master'
    commit = {
        'author': {
            'email': 'dvander@google.com',
            'name': 'David Anderson',
            'time': 'Tue Feb 18 23:29:44 2020 -0800'
        },
        'commit': 'ab9c7e6d04c896ddcbfc2e3bc99ab00e6a892288',
        'message': 'Exclude holes from the block map.'
    }
    label = Diff.INSERT

    buf = querier._build(repo, branch, commit, label)
    assert len(buf) == 1

    commit1 = {
        'committer': {
            'time': 'Tue Feb 18 23:29:44 2020 -0800'
        }
    }
    commit2 = {
        'committer': {
            'time': 'Tue Feb 18 23:29:45 2020 -0800'
        }
    }

    ret = querier._ahead(commit1, commit2)
    assert ret is True

    repo = 'platform/art'
    commit1 = {
        'branch': 'master',
        'commit': '7ffa83e83d9f2f6533ba40695b60beca51c453fc'
    }
    commit2 = {
        'branch': 'master',
        'commit': '587fc20905e241750152831bc27ffe99b576a535'
    }

    try:
        _ = querier._commits(repo, commit1, commit2, True)
    except requests.exceptions.InvalidSchema:
        pass

    repo = 'platform/art'
    commit1 = {
        'branch': 'master',
        'commit': '7ffa83e83d9f2f6533ba40695b60beca51c453fc'
    }
    commit2 = {
        'branch': 'master',
        'commit': '587fc20905e241750152831bc27ffe99b576a535'
    }

    try:
        _ = querier._commit1(repo, commit1, commit2)
    except requests.exceptions.InvalidSchema:
        pass

    repo = 'platform/art'
    commit1 = {
        'branch': 'master',
        'commit': '7ffa83e83d9f2f6533ba40695b60beca51c453fc'
    }
    commit2 = {
        'branch': 'master',
        'commit': '587fc20905e241750152831bc27ffe99b576a535'
    }
    label = Diff.CHANGE

    try:
        _ = querier._diff(repo, commit1, commit2, label)
    except requests.exceptions.InvalidSchema:
        pass

    buf = {
        'change': {
            'device/common': [
                {
                    'branch': 'master',
                    'commit': '7ffa83e83d9f2f6533ba40695b60beca51c453fc'
                },
                {
                    'branch': 'master',
                    'commit': '587fc20905e241750152831bc27ffe99b576a535'
                }
            ]
        }
    }

    try:
        buf = querier._fetch(buf, Diff.CHANGE)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)

    buf = {
        'delete': {
            'platform/build/kati': [
                {
                    'branch': 'master',
                    'commit': '831dcffa2be201e2158c1851d9a9ad7abd6293ce'
                },
                {}
            ]
        }
    }

    try:
        buf = querier._fetch(buf, Diff.DELETE)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)

    buf = {
        'insert': {
            'platform/build': [
                {},
                {
                    'branch': 'master',
                    'commit': '5832bf1f5a949bc32a9b8f57ed46cb7f06606fe6'
                }
            ]
        }
    }

    try:
        buf = querier._fetch(buf, Diff.INSERT)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)
