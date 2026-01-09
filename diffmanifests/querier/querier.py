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

    def _get_commits_with_variants(self, repo, branch, commit):
        candidates = [branch]
        if branch and not branch.startswith('refs/'):
            candidates.extend([f'refs/heads/{branch}', f'refs/tags/{branch}'])
        for b in candidates:
            try:
                data = self.gitiles.commits(repo, b, commit)
            except StopIteration:
                data = None
            if data is not None and len(data.get('log', [])) != 0:
                return data
        return None

    def _build(self, repo, branch, commit, label):
        def _query(commit):
            buf = self.gerrit.query('commit:' + commit, 0)
            if buf is None or len(buf) != 1:
                return '', '', []

            # Construct the change URL based on Gerrit instance type
            gerrit_url = self.gerrit.url()
            # Remove /a suffix if present (used for authenticated access)
            if gerrit_url.endswith('/a'):
                gerrit_url = gerrit_url[:-2]

            change_number = str(buf[0]['_number'])

            # For self-hosted Gerrit (non-googlesource), add /c/ prefix
            if 'googlesource.com' not in gerrit_url:
                change_url = gerrit_url + '/c/' + repo + '/+/' + change_number
            else:
                change_url = gerrit_url + '/' + change_number

            return change_url, buf[0].get('topic', ''), buf[0].get('hashtags', [])

        change, topic, hashtags = _query(commit['commit'])
        return [{
            Commit.AUTHOR: '%s <%s>' % (commit['author']['name'], commit['author']['email']),
            Commit.BRANCH: branch,
            Commit.CHANGE: change,
            Commit.COMMIT: commit['commit'],
            Commit.COMMITTER: '%s <%s>' % (commit['committer']['name'], commit['committer']['email']),
            Commit.DATE: commit['author']['time'],
            Commit.DIFF: label.upper(),
            Commit.HASHTAGS: hashtags,
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
            commits = self._get_commits_with_variants(repo, commit2[Repo.BRANCH], commit2[Repo.COMMIT])
            if commits is None:
                return [], None, False
            completed = False
            next = commits.get('next', None) if backward else commits.get('previous', None)
            for item in commits['log']:
                if item['commit'] == commit1[Repo.COMMIT] or item['commit'].startswith(commit1[Repo.COMMIT]):
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
        # Try to get commits from commit2's history using the branch (with variants)
        commits = self._get_commits_with_variants(repo, commit2[Repo.BRANCH], commit2[Repo.COMMIT])
        if commits is None:
            # Fallback: try using commit hash directly (rare for +log, but attempt variants)
            commits = self._get_commits_with_variants(repo, commit2[Repo.COMMIT], commit2[Repo.COMMIT])
            if commits is None:
                Logger.warn('_commit1: Failed to get commits for repo: %s with branch variants and commit hash' % repo)
                return None, ''

        iterations = 0
        max_iterations = 100  # Prevent infinite loops
        checked_commits = []
        while iterations < max_iterations:
            iterations += 1
            commit = None
            for item in commits.get('log', []):
                checked_commits.append(item['commit'][:8])  # Store first 8 chars for logging
                # Check if this commit exists in commit1's history by querying from commit1
                # Try branch variants to find the intersection
                data = self._get_commits_with_variants(repo, commit1[Repo.BRANCH], item['commit'])
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
                Logger.warn('_commit1: No more commits to check (pagination ended) for repo: %s after %d iterations (checked: %s)' % (repo, iterations, ', '.join(checked_commits)))
                break
            commits = self._get_commits_with_variants(repo, commit2[Repo.BRANCH], data)
            if commits is None:
                Logger.warn('_commit1: Failed to get next page of commits for repo: %s' % repo)
                break

        if iterations >= max_iterations:
            Logger.warn('_commit1: Reached max iterations (%d) for repo: %s' % (max_iterations, repo))

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
            Logger.warn('Failed to find common commit for repo: %s (commit1: %s, commit2: %s), treating as independent commits' % (repo, commit1[Repo.COMMIT], commit2[Repo.COMMIT]))
            # Fallback: treat commit2 as an added commit and commit1 as context
            data2 = self.gitiles.commit(repo, commit2[Repo.COMMIT])
            if data2 is not None:
                buf.extend(self._build(repo, commit2[Repo.BRANCH], data2, Label.ADD_COMMIT))
            return buf

        # Try with branch first, if it fails, use commit hash
        commits, status = self._commits(repo, commit, commit2, True)
        if status is False:
            # Retry with commit hash as branch
            commit2_with_hash_branch = {
                Repo.BRANCH: commit2[Repo.COMMIT],
                Repo.COMMIT: commit2[Repo.COMMIT]
            }
            commits, status = self._commits(repo, commit, commit2_with_hash_branch, True)
            if status is False:
                Logger.warn('Failed to get commits between common commit and commit2 for repo: %s (tried both branch and commit hash)' % repo)
                return []
        for item in commits:
            buf.extend(self._build(repo, commit2[Repo.BRANCH], item, Label.ADD_COMMIT))
        if commit[Repo.COMMIT] != commit1[Repo.COMMIT]:
            if label == Label.ADD_COMMIT:
                commits, status = self._commits(repo, commit1, commit, True)
            else:
                commits, status = self._commits(repo, commit, commit1, True)
            if status is False:
                Logger.warn('Failed to get commits between commit1 and common commit for repo: %s' % repo)
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
            # Extract actual repo name from the commit data if available
            # For projects with duplicate names, use the 'name' field from Repo
            repo_name = key
            if val and len(val) > 0:
                # Check first non-empty dict in the list
                for item in val:
                    if item and Repo.NAME in item:
                        repo_name = item[Repo.NAME]
                        break
            buf.extend(_helper(repo_name, val, label))
        return buf

    def run(self, data):
        buf = []
        buf.extend(self._fetch(data, Label.ADD_REPO))
        buf.extend(self._fetch(data, Label.REMOVE_REPO))
        buf.extend(self._fetch(data, Label.UPDATE_REPO))
        return buf
