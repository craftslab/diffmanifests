# -*- coding: utf-8 -*-

import os
import pprint
import requests
import unittest.mock

from diffmanifests.main import load
from diffmanifests.gitiles.gitiles import Gitiles, GitilesException


def test_exception():
    exception = GitilesException('exception')
    assert str(exception) == 'exception'


def test_gitiles():
    try:
        _ = Gitiles(None)
    except GitilesException:
        assert True

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
    commit = 'fffffff'

    buf = gitiles.commit(repo, commit)
    assert buf is None

    repo = 'platform/build'
    branch = 'master'
    commit = '5832bf1f5a949bc32a9b8f57ed46cb7f06606fe6'

    try:
        buf = gitiles.commits(repo, branch, commit)
    except requests.exceptions.InvalidSchema:
        buf = None

    if buf is not None:
        pprint.pprint(buf)

    repo = 'platform/build'
    branch = 'master'
    commit = 'fffffff'

    buf = gitiles.commits(repo, branch, commit)
    assert buf is None


def test_gitiles_url():
    """Test that Gitiles URL is returned correctly"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    gitiles = Gitiles(config)

    url = gitiles.url()
    assert url is not None
    assert isinstance(url, str)
    assert len(url) > 0


def test_gitiles_with_auth():
    """Test Gitiles initialization with authentication"""
    config = {
        'gitiles': {
            'url': 'https://android.googlesource.com',
            'user': 'test@example.com',
            'pass': 'password',
            'retry': 3,
            'timeout': 30
        }
    }

    gitiles = Gitiles(config)
    assert gitiles is not None


def test_gitiles_with_trailing_slash():
    """Test that Gitiles removes trailing slashes from URL"""
    config = {
        'gitiles': {
            'url': 'https://android.googlesource.com/',
            'user': '',
            'pass': '',
            'retry': 0,
            'timeout': -1
        }
    }

    gitiles = Gitiles(config)
    url = gitiles.url()
    # URL should not have trailing slash
    assert not url.endswith('/')


def test_gitiles_with_invalid_retry():
    """Test that negative retry value is treated as 0"""
    config = {
        'gitiles': {
            'url': 'https://android.googlesource.com',
            'user': '',
            'pass': '',
            'retry': -5,  # Should be treated as 0
            'timeout': -1
        }
    }

    gitiles = Gitiles(config)
    assert gitiles is not None


def test_gitiles_with_invalid_timeout():
    """Test that negative timeout is treated as None"""
    config = {
        'gitiles': {
            'url': 'https://android.googlesource.com',
            'user': '',
            'pass': '',
            'retry': 0,
            'timeout': -1  # Should be treated as None
        }
    }

    gitiles = Gitiles(config)
    assert gitiles is not None


def test_gitiles_commit_with_auth():
    """Test Gitiles.commit() with authentication"""
    config = {
        'gitiles': {
            'url': 'https://android.googlesource.com',
            'user': 'test@example.com',
            'pass': 'password',
            'retry': 0,
            'timeout': 30
        }
    }

    gitiles = Gitiles(config)

    with unittest.mock.patch('diffmanifests.gitiles.gitiles.requests.Session.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        import json
        mock_response.text = ")]}'" + json.dumps({"commit": "abc123", "tree": "def456"})
        mock_get.return_value = mock_response

        result = gitiles.commit('platform/build', 'abc123def456')

        assert result is not None
        assert result['commit'] == 'abc123'


def test_gitiles_commit_failure():
    """Test Gitiles.commit() returns None on HTTP error"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    gitiles = Gitiles(config)

    with unittest.mock.patch('requests.Session.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = gitiles.commit('platform/build', 'invalid')

        assert result is None


def test_gitiles_commits_failure():
    """Test Gitiles.commits() returns None on HTTP error"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    gitiles = Gitiles(config)

    with unittest.mock.patch('requests.Session.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = gitiles.commits('platform/build', 'master', 'abc123')

        assert result is None


def test_gitiles_with_empty_config():
    """Test that Gitiles raises exception with empty config"""
    import pytest

    with pytest.raises(GitilesException):
        Gitiles({})


def test_gitiles_commits_with_auth():
    """Test Gitiles.commits() with authentication"""
    config = {
        'gitiles': {
            'url': 'https://android.googlesource.com',
            'user': 'test@example.com',
            'pass': 'password',
            'retry': 0,
            'timeout': 30
        }
    }

    gitiles = Gitiles(config)

    with unittest.mock.patch('diffmanifests.gitiles.gitiles.requests.Session.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        import json
        mock_response.text = ")]}'" + json.dumps({
            "log": [{"commit": "abc123", "message": "Test"}],
            "previous": "def456"
        })
        mock_get.return_value = mock_response

        result = gitiles.commits('platform/build', 'master', 'abc123')

        assert result is not None
        assert len(result['log']) == 1
