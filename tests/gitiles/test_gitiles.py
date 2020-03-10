# -*- coding: utf-8 -*-

import os
import pprint
import requests

from diffmanifests.main import load
from diffmanifests.gitiles.gitiles import Gitiles, GitilesException


def test_exception():
    exception = GitilesException('exception')
    assert str(exception) == 'exception'


def test_gitiles():
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    gitiles = Gitiles(config)
    assert gitiles is not None

    repo = 'platform/build'
    commit = '5832bf1f5a949bc32a9b8f57ed46cb7f06606fe6'

    try:
        buf = gitiles.commit(repo, commit)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)

    repo = 'platform/build'
    branch = 'master'
    commit = '5832bf1f5a949bc32a9b8f57ed46cb7f06606fe6'

    try:
        buf = gitiles.commits(repo, branch, commit)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)
