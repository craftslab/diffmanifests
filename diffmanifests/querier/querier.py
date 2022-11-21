# -*- coding: utf-8 -*-

import datetime

from ..gerrit.gerrit import Gerrit
from ..gitiles.gitiles import Gitiles
from ..logger.logger import Logger
from ..proto.proto import Commit, Label, Repo


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
        self.gerrit = Gerrit(config)
        self.gitiles = Gitiles(config)

    def _build(self, repo, branch, commit, label):
        def _query(commit):
            buf = self.gerrit.query('commit:' + commit, 0)
            if buf is None or len(buf) != 1:
                return '', ''
            return self.gerrit.url().replace('/a', '/') + str(buf[0]['_number']), buf[0].get('topic', '')

        change, topic = _query(commit['commit'])
        return [{
            Commit.AUTHOR: '%s <%s>' % (commit['author']['name'], commit['author']['email']),
            Commit.BRANCH: branch,
            Commit.CHANGE: change,
            Commit.COMMIT: commit['commit'],
            Commit.COMMITTER: '%s <%s>' % (commit['committer']['name'], commit['committer']['email']),
            Commit.DATE: commit['author']['time'],
            Commit.DIFF: label.upper(),
            Commit.MESSAGE: commit['message'].strip(),
            Commit.REPO: repo,
            Commit.TOPIC: topic,
            Commit.URL: self.gitiles.url() + '/' + repo + '/+/' + commit['commit']
        }]

    def _ahead(self, commit1, commit2):
        def _helper(data):
            for item in data:
                if '\u4e00' <= item <= '\u9fff':
                    return True
            return False
        buf1 = " ".join(commit1['committer']['time'].split(" ")[1:])
        if _helper(buf1) is True:
            buf1 = datetime.datetime.strptime(buf1, '%m月 %d %H:%M:%S %Y %z')
        else:
            buf1 = datetime.datetime.strptime(buf1, '%b %d %H:%M:%S %Y %z')
        buf2 = " ".join(commit2['committer']['time'].split(" ")[1:])
        if _helper(buf2) is True:
            buf2 = datetime.datetime.strptime(buf2, '%m月 %d %H:%M:%S %Y %z')
        else:
            buf2 = datetime.datetime.strptime(buf2, '%b %d %H:%M:%S %Y %z')
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
        commits = self.gitiles.commits(repo, commit2[Repo.BRANCH], commit2[Repo.COMMIT])
        if commits is None:
            return None, ''
        while True:
            commit = None
            for item in commits.get('log', []):
                data = self.gitiles.commits(repo, commit1[Repo.BRANCH], item['commit'])
                if data is not None and len(data['log']) != 0:
                    commit = {
                        Repo.BRANCH: commit1[Repo.BRANCH],
                        Repo.COMMIT: item['commit']
                    }
                    break
            if commit is not None:
                break
            data = commits.get('next', None)
            if data is None:
                break
            commits = self.gitiles.commits(repo, commit2[Repo.BRANCH], data)
        if commit is None:
            return None, ''
        data1 = self.gitiles.commit(repo, commit1[Repo.COMMIT])
        data2 = self.gitiles.commit(repo, commit[Repo.COMMIT])
        if data1 is None or data2 is None:
            return None, ''
        if self._ahead(data1, data2) is True:
            label = Label.ADD_COMMIT
        else:
            label = Label.REMOVE_COMMIT
        return commit, label

    def _diff(self, repo, commit1, commit2):
        buf = []
        commit, label = self._commit1(repo, commit1, commit2)
        if commit is None:
            return []
        commits, status = self._commits(repo, commit, commit2, True)
        if status is False:
            return []
        for item in commits:
            buf.extend(self._build(repo, commit2[Repo.BRANCH], item, Label.ADD_COMMIT))
        if commit[Repo.COMMIT] != commit1[Repo.COMMIT]:
            if label == Label.ADD_COMMIT:
                commits, status = self._commits(repo, commit1, commit, True)
            else:
                commits, status = self._commits(repo, commit, commit1, True)
            if status is False:
                return []
            for item in commits:
                buf.extend(self._build(repo, commit1[Repo.BRANCH], item, label))
        return buf

    def _fetch(self, data, label):
        def _helper(repo, commit, label):
            buf1, buf2 = commit
            Logger.info(label + ': ' + repo)
            if label == Label.ADD_REPO:
                data = self.gitiles.commit(repo, buf2[Repo.COMMIT])
                if data is None:
                    return []
                return self._build(repo, buf2[Repo.BRANCH], data, label)
            elif label == Label.REMOVE_REPO:
                data = self.gitiles.commit(repo, buf1[Repo.COMMIT])
                if data is None:
                    return []
                return self._build(repo, buf1[Repo.BRANCH], data, label)
            elif label == Label.UPDATE_REPO:
                return self._diff(repo, buf1, buf2)
            else:
                return []

        buf = []
        for key, val in data.get(label, {}).items():
            buf.extend(_helper(key, val, label))
        return buf

    def run(self, data):
        buf = []
        buf.extend(self._fetch(data, Label.ADD_REPO))
        buf.extend(self._fetch(data, Label.REMOVE_REPO))
        buf.extend(self._fetch(data, Label.UPDATE_REPO))
        return buf
