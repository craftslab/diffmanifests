# -*- coding: utf-8 -*-

import datetime

from ..gitiles.gitiles import Gitiles
from ..proto.proto import Commit, Diff, Repo


class QuerierException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Querier(object):
    def __init__(self, config=None):
        if config is None:
            raise QuerierException('config invalid')
        self.gitiles = Gitiles(config)

    def _build(self, repo, branch, commit, label):
        return [{
            Commit.AUTHOR: '%s <%s>' % (commit['author']['name'], commit['author']['email']),
            Commit.BRANCH: branch,
            Commit.COMMIT: commit['commit'],
            Commit.DATE: commit['author']['time'],
            Commit.DIFF: label.upper(),
            Commit.MESSAGE: commit['message'].split('\n')[0],
            Commit.REPO: repo,
            Commit.URL: self.gitiles.url() + '/' + repo + '/+/' + commit['commit']
        }]

    def _ahead(self, commit1, commit2):
        buf1 = datetime.datetime.strptime(commit1['committer']['time'], '%a %b %d %H:%M:%S %Y %z')
        buf2 = datetime.datetime.strptime(commit2['committer']['time'], '%a %b %d %H:%M:%S %Y %z')
        return buf2 > buf1

    def _commits(self, repo, commit1, commit2, backward):
        def _helper(repo, commit1, commit2, backward):
            buf = []
            commit = self.gitiles.commit(repo, commit1[Repo.COMMIT])
            if commit is None:
                return [], None, False
            commits = self.gitiles.commits(repo, commit2[Repo.BRANCH], commit2[Repo.COMMIT])
            if commits is None:
                return [], None, False
            completed = False
            next = commits.get('next', None) if backward else commits.get('previous', None)
            for item in commits['log']:
                if item['commit'] == commit1[Repo.COMMIT]:
                    completed = True
                    break
                if (backward and self._ahead(item, commit)) \
                        or (not backward and self._ahead(commit, item)):
                    next = None
                    break
                buf.append(item)
            return buf, next, completed

        buf = []
        while True:
            commits, next, completed = _helper(repo, commit1, commit2, backward)
            buf.extend(commits)
            if completed is True:
                status = True
                break
            else:
                if next is None:
                    status = False
                    break
            commit2 = {
                Repo.BRANCH: commit2[Repo.BRANCH],
                Repo.COMMIT: next
            }
        return buf, status

    def _commit1(self, repo, commit1, commit2):
        if commit1[Repo.BRANCH] == commit2[Repo.BRANCH]:
            return commit1
        commit = {
            Repo.BRANCH: commit2[Repo.BRANCH],
            Repo.COMMIT: commit1[Repo.COMMIT]
        }
        commits2, status = self._commits(repo, commit, commit2, True)
        buf2 = []
        if status is True:
            buf2.append(commit[Repo.COMMIT])
        buf2.extend([item['commit'] for item in commits2])
        commit = {
            Repo.BRANCH: commit1[Repo.BRANCH],
            Repo.COMMIT: commit2[Repo.COMMIT]
        }
        commits1, _ = self._commits(repo, commit, commit1, False)
        commit = None
        for item in commits1:
            if item['commit'] in buf2:
                commit = {
                    Repo.BRANCH: commit1[Repo.BRANCH],
                    Repo.COMMIT: item['commit']
                }
                break
        return commit

    def _diff(self, repo, commit1, commit2, label):
        buf = []
        commit = self._commit1(repo, commit1, commit2)
        if commit is None:
            return []
        commits, status = self._commits(repo, commit, commit2, True)
        if status is False:
            return []
        for item in commits:
            buf.extend(self._build(repo, commit2[Repo.BRANCH], item, label))
        if commit[Repo.COMMIT] != commit1[Repo.COMMIT]:
            commits, status = self._commits(repo, commit1, commit, True)
            if status is False:
                return []
            for item in commits:
                buf.extend(self._build(repo, commit1[Repo.BRANCH], item, label))
        return buf

    def _fetch(self, data, label):
        def _helper(repo, commit, label):
            buf1, buf2 = commit
            if label == Diff.CHANGE:
                return self._diff(repo, buf1, buf2, label)
            elif label == Diff.DELETE:
                return self._build(repo, buf1[Repo.BRANCH], self.gitiles.commit(repo, buf1[Repo.COMMIT]), label)
            elif label == Diff.INSERT:
                return self._build(repo, buf2[Repo.BRANCH], self.gitiles.commit(repo, buf2[Repo.COMMIT]), label)
            else:
                return []

        buf = []
        for key, val in data.get(label, {}).items():
            buf.extend(_helper(key, val, label))
        return buf

    def run(self, data):
        buf = []
        buf.extend(self._fetch(data, Diff.CHANGE))
        buf.extend(self._fetch(data, Diff.DELETE))
        buf.extend(self._fetch(data, Diff.INSERT))
        return buf
