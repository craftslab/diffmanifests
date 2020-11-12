# -*- coding: utf-8 -*-


"""Prototype
{
    "add repo": {
        "REPO": [
            {},
            {
                "branch": BRANCH,
                "commit": COMMIT,
                "diff": "add commit"
            }
        ]
    },
    "remove repo": {
        "REPO": [
            {
                "branch": BRANCH,
                "commit": COMMIT,
                "diff": "remove commit"
            },
            {}
        ]
    },
    "update repo": {
        "REPO": [
            {
                "branch": BRANCH,
                "commit": COMMIT,
                "diff": "add commit"
            },
            {
                "branch": BRANCH,
                "commit": COMMIT,
                "diff": "remove commit"
            }
        ]
    }
}
"""


class Commit:
    AUTHOR = 'author'
    BRANCH = 'branch'
    CHANGE = 'change'
    COMMIT = 'commit'
    COMMITTER = 'committer'
    DATE = 'date'
    DIFF = 'diff'
    MESSAGE = 'message'
    REPO = 'repo'
    TOPIC = 'topic'
    URL = 'url'


class Label:
    ADD_COMMIT = 'add commit'
    ADD_REPO = 'add repo'
    REMOVE_COMMIT = 'remove commit'
    REMOVE_REPO = 'remove repo'
    UPDATE_REPO = 'update repo'


class Repo:
    BRANCH = 'branch'
    COMMIT = 'commit'
    DIFF = 'diff'
