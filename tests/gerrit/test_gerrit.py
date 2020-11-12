# -*- coding: utf-8 -*-

from diffmanifests.gerrit.gerrit import Gerrit, GerritException


def test_exception():
    exception = GerritException('exception')
    assert str(exception) == 'exception'


def test_gerrit():
    config = {
        "gerrit": {
            "pass": "",
            "query": {
                "option": ["CURRENT_REVISION"]
            },
            "url": "https://android-review.googlesource.com",
            "user": ""
        }
    }

    gerrit = Gerrit(config)
    assert gerrit is not None

    buf = gerrit.get(1358810)
    assert buf is not None

    buf = gerrit.query('change:1358810', 0)
    assert buf is not None
