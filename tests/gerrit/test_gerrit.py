# -*- coding: utf-8 -*-

import unittest.mock

from diffmanifests.gerrit.gerrit import Gerrit, GerritException


def test_exception():
    exception = GerritException('exception')
    assert str(exception) == 'exception'


def test_gerrit():
    try:
        _ = Gerrit(None)
    except GerritException:
        assert True

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

    buf = gerrit.get(0000000)
    assert buf is None

    buf = gerrit.query('change:1358810', 0)
    assert buf is not None

    buf = gerrit.query('change:0000000', 0)
    assert buf is None


def test_gerrit_hashtags_in_response():
    """Test that Gerrit query can handle hashtags in response"""
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

    # Mock response with hashtags
    mock_response_data = [
        {
            "_number": 123456,
            "project": "test/project",
            "branch": "master",
            "hashtags": ["feature", "test", "important"],
            "topic": "test-topic",
            "subject": "Test change with hashtags",
            "status": "NEW"
        }
    ]

    with unittest.mock.patch('requests.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        # Proper JSON formatting with Gerrit prefix
        import json
        mock_response.text = ")]}\'\n" + json.dumps(mock_response_data)
        mock_get.return_value = mock_response

        result = gerrit.query('commit:abc123', 0)

        assert result is not None
        assert len(result) == 1
        assert 'hashtags' in result[0]
        assert result[0]['hashtags'] == ["feature", "test", "important"]


def test_gerrit_response_without_hashtags():
    """Test that Gerrit query handles response without hashtags field"""
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

    # Mock response without hashtags
    mock_response_data = [{
        "_number": 123456,
        "project": "test/project",
        "branch": "master",
        "topic": "test-topic",
        "subject": "Test change without hashtags",
        "status": "NEW"
    }]

    with unittest.mock.patch('requests.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        # Proper JSON formatting with Gerrit prefix
        import json
        mock_response.text = ")]}\'\n" + json.dumps(mock_response_data)
        mock_get.return_value = mock_response

        result = gerrit.query('commit:abc123', 0)

        assert result is not None
        assert len(result) == 1
        # Should not have hashtags field, which is expected
        assert 'hashtags' not in result[0] or result[0].get('hashtags') is None


def test_gerrit_url():
    """Test that Gerrit URL is returned correctly"""
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
    assert gerrit.url() == "https://android-review.googlesource.com"


def test_gerrit_url_with_auth():
    """Test that Gerrit URL has /a suffix when auth is configured"""
    config = {
        "gerrit": {
            "pass": "password",
            "query": {
                "option": ["CURRENT_REVISION"]
            },
            "url": "https://android-review.googlesource.com",
            "user": "admin"
        }
    }

    gerrit = Gerrit(config)
    assert gerrit.url() == "https://android-review.googlesource.com/a"


def test_gerrit_get_with_auth():
    """Test that Gerrit.get() works with authentication"""
    config = {
        "gerrit": {
            "pass": "password",
            "query": {
                "option": ["CURRENT_REVISION"]
            },
            "url": "https://test.example.com",
            "user": "admin"
        }
    }

    gerrit = Gerrit(config)

    with unittest.mock.patch('diffmanifests.gerrit.gerrit.requests.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        import json
        mock_response.text = ")]}'" + json.dumps({"_number": 123, "subject": "Test"})
        mock_get.return_value = mock_response

        result = gerrit.get(123)

        assert result is not None
        assert result['_number'] == 123
        # Verify auth was passed to requests.get
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['auth'] == ('admin', 'password')


def test_gerrit_get_failure():
    """Test that Gerrit.get() returns None on HTTP error"""
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

    with unittest.mock.patch('requests.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = gerrit.get(999999)

        assert result is None


def test_gerrit_query_with_auth():
    """Test that Gerrit.query() works with authentication"""
    config = {
        "gerrit": {
            "pass": "password",
            "query": {
                "option": ["CURRENT_REVISION"]
            },
            "url": "https://test.example.com",
            "user": "admin"
        }
    }

    gerrit = Gerrit(config)

    with unittest.mock.patch('diffmanifests.gerrit.gerrit.requests.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        import json
        mock_response.text = ")]}'" + json.dumps([{"_number": 123, "subject": "Test"}])
        mock_get.return_value = mock_response

        result = gerrit.query('status:open', 0)

        assert result is not None
        assert len(result) == 1
        # Verify auth was passed to requests.get
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['auth'] == ('admin', 'password')


def test_gerrit_query_failure():
    """Test that Gerrit.query() returns None on HTTP error"""
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

    with unittest.mock.patch('requests.get') as mock_get:
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = gerrit.query('status:open', 0)

        assert result is None
