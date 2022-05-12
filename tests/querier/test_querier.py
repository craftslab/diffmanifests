# -*- coding: utf-8 -*-

import os
import pprint
import requests

from diffmanifests.main import load
from diffmanifests.proto.proto import Label
from diffmanifests.querier.querier import Querier, QuerierException


def test_exception():
    exception = QuerierException('exception')
    assert str(exception) == 'exception'


def test_querier():
    try:
        _ = Querier(None)
    except QuerierException:
        assert True

    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    querier = Querier(config)
    assert querier is not None

    repo = 'platform/build'
    branch = 'master'
    commit = {
        'author': {
            'email': 'tomcherry@google.com',
            'name': 'Tom Cherry',
            'time': 'Tue Feb 18 20:54:58 2020 +0000'
        },
        'commit': 'c9d21efbbfffd0fc41369a34e2f600c3865ac03b',
        'committer': {
            'email': 'tomcherry@google.com',
            'name': 'Tom Cherry',
            'time': 'Tue Feb 18 20:54:58 2020 +0000'
        },
        'message': 'Merge "Make oemaids_headers available to vendor."'
                   ''
                   'Detailed description'
                   ''
                   'Change-Id: 12345678'
    }

    label = Label.ADD_COMMIT

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

    repo = 'device/common'
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

    repo = 'device/common'
    commit1 = {
        'branch': 'master',
        'commit': 'eeeeeee'
    }
    commit2 = {
        'branch': 'master',
        'commit': 'fffffff'
    }

    _, status = querier._commits(repo, commit1, commit2, True)
    assert status is False

    repo = 'device/common'
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

    repo = 'device/common'
    commit1 = {
        'branch': 'master',
        'commit': 'eeeeeee'
    }
    commit2 = {
        'branch': 'master',
        'commit': 'fffffff'
    }

    commit, _ = querier._commit1(repo, commit1, commit2)
    assert commit is None

    repo = 'device/common'
    commit1 = {
        'branch': 'master',
        'commit': '7ffa83e83d9f2f6533ba40695b60beca51c453fc'
    }
    commit2 = {
        'branch': 'master',
        'commit': '587fc20905e241750152831bc27ffe99b576a535'
    }

    try:
        _ = querier._diff(repo, commit1, commit2)
    except requests.exceptions.InvalidSchema:
        pass

    repo = 'device/common'
    commit1 = {
        'branch': 'master',
        'commit': 'eeeeeee'
    }
    commit2 = {
        'branch': 'master',
        'commit': 'fffffff'
    }

    buf = querier._diff(repo, commit1, commit2)
    assert len(buf) == 0

    buf = {
        'add repo': {
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
        buf = querier._fetch(buf, Label.ADD_REPO)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)

    buf = {
        'remove repo': {
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
        buf = querier._fetch(buf, Label.REMOVE_REPO)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)

    buf = {
        'update repo': {
            'device/common': [
                {
                    'branch': 'master',
                    'commit': '7ffa83e83d9f2f6533ba40695b60beca51c453fc',
                    "diff": "add commit"
                },
                {
                    'branch': 'master',
                    'commit': '587fc20905e241750152831bc27ffe99b576a535',
                    "diff": "remove commit"
                }
            ]
        }
    }

    try:
        buf = querier._fetch(buf, Label.UPDATE_REPO)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)
