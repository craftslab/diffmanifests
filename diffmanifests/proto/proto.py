# -*- coding: utf-8 -*-


"""Prototype
{
    "change": {
        "REPO": [
            {
                "branch": BRANCH,
                "commit": COMMIT
            },
            {
                "branch": BRANCH,
                "commit": COMMIT
            }
        ]
    },
    "delete": {
        "REPO": [
            {
                "branch": BRANCH,
                "commit": COMMIT
            },
            {}
        ]
    },
    "insert": {
        "REPO": [
            {},
            {
                "branch": BRANCH,
                "commit": COMMIT
            }
        ]
    }
}
"""


class Commit:
    AUTHOR = 'author'
    BRANCH = 'branch'
    COMMIT = 'commit'
    DATE = 'date'
    DIFF = 'diff'
    MESSAGE = 'message'
    REPO = 'repo'
    URL = 'url'


class Diff:
    CHANGE = 'change'
    DELETE = 'delete'
    INSERT = 'insert'


class Repo:
    BRANCH = 'branch'
    COMMIT = 'commit'
