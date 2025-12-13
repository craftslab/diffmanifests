# -*- coding: utf-8 -*-

"""Tests for proto constants and structures"""

from diffmanifests.proto.proto import Commit, Label, Repo


def test_commit_constants():
    """Test that all Commit constants are properly defined"""
    expected_constants = [
        'AUTHOR', 'BRANCH', 'CHANGE', 'COMMIT', 'COMMITTER',
        'DATE', 'DIFF', 'HASHTAGS', 'MESSAGE', 'REPO', 'TOPIC', 'URL'
    ]

    for constant in expected_constants:
        assert hasattr(Commit, constant), f"Commit.{constant} should be defined"
        assert isinstance(getattr(Commit, constant), str), f"Commit.{constant} should be a string"

    # Test specific values
    assert Commit.HASHTAGS == 'hashtags'
    assert Commit.AUTHOR == 'author'
    assert Commit.BRANCH == 'branch'
    assert Commit.CHANGE == 'change'
    assert Commit.COMMIT == 'commit'
    assert Commit.COMMITTER == 'committer'
    assert Commit.DATE == 'date'
    assert Commit.DIFF == 'diff'
    assert Commit.MESSAGE == 'message'
    assert Commit.REPO == 'repo'
    assert Commit.TOPIC == 'topic'
    assert Commit.URL == 'url'


def test_label_constants():
    """Test that all Label constants are properly defined"""
    expected_constants = [
        'ADD_COMMIT', 'ADD_REPO', 'REMOVE_COMMIT', 'REMOVE_REPO', 'UPDATE_REPO'
    ]

    for constant in expected_constants:
        assert hasattr(Label, constant), f"Label.{constant} should be defined"
        assert isinstance(getattr(Label, constant), str), f"Label.{constant} should be a string"

    # Test specific values
    assert Label.ADD_COMMIT == 'add commit'
    assert Label.ADD_REPO == 'add repo'
    assert Label.REMOVE_COMMIT == 'remove commit'
    assert Label.REMOVE_REPO == 'remove repo'
    assert Label.UPDATE_REPO == 'update repo'


def test_repo_constants():
    """Test that all Repo constants are properly defined"""
    expected_constants = ['BRANCH', 'COMMIT', 'DIFF']

    for constant in expected_constants:
        assert hasattr(Repo, constant), f"Repo.{constant} should be defined"
        assert isinstance(getattr(Repo, constant), str), f"Repo.{constant} should be a string"

    # Test specific values
    assert Repo.BRANCH == 'branch'
    assert Repo.COMMIT == 'commit'
    assert Repo.DIFF == 'diff'


def test_hashtags_integration():
    """Test that hashtags constant can be used properly"""
    # Create a mock commit dictionary using the constants
    commit_data = {
        Commit.AUTHOR: 'Test Author <test@example.com>',
        Commit.BRANCH: 'master',
        Commit.CHANGE: 'http://gerrit.example.com/12345',
        Commit.COMMIT: 'abc123def456',
        Commit.COMMITTER: 'Test Committer <test@example.com>',
        Commit.DATE: '2023-01-01 12:00:00 +0000',
        Commit.DIFF: 'ADD COMMIT',
        Commit.HASHTAGS: ['feature', 'urgent', 'test'],
        Commit.MESSAGE: 'Test commit message',
        Commit.REPO: 'test/repo',
        Commit.TOPIC: 'test-topic',
        Commit.URL: 'http://gitiles.example.com/test/repo/+/abc123def456'
    }

    # Verify all fields are accessible
    assert commit_data[Commit.HASHTAGS] == ['feature', 'urgent', 'test']
    assert isinstance(commit_data[Commit.HASHTAGS], list)
    assert len(commit_data[Commit.HASHTAGS]) == 3

    # Verify all expected fields are present
    for field in [Commit.AUTHOR, Commit.BRANCH, Commit.CHANGE, Commit.COMMIT,
                  Commit.COMMITTER, Commit.DATE, Commit.DIFF, Commit.HASHTAGS,
                  Commit.MESSAGE, Commit.REPO, Commit.TOPIC, Commit.URL]:
        assert field in commit_data, f"Field {field} should be in commit data"

def test_repo_name_constant():
    """Test that Repo has NAME constant"""
    assert hasattr(Repo, 'NAME'), "Repo.NAME should be defined"
    assert Repo.NAME == 'name'
    assert isinstance(Repo.NAME, str)