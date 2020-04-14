# -*- coding: utf-8 -*-

import jsondiff

from ..proto.proto import Diff, Repo


class DifferException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Differ(object):
    def __init__(self, config=None):
        if config is None:
            pass

    def _revision(self, data):
        if 'default' not in data['manifest'] or '@revision' not in data['manifest']['default']:
            return ''
        return data['manifest']['default']['@revision']

    def _commit(self, data, diff, label):
        def _helper(data, project, commit, label):
            if label == Diff.DELETE:
                buf = [
                    {
                        Repo.BRANCH: project.get('@upstream', self._revision(data)),
                        Repo.COMMIT: project.get('@revision', '')
                    },
                    {}
                ]
            elif label == Diff.INSERT:
                buf = [
                    {},
                    {
                        Repo.BRANCH: project.get('@upstream', self._revision(data)),
                        Repo.COMMIT: project.get('@revision', '')
                    }
                ]
            else:
                buf = [
                    {},
                    {}
                ]
            commit[project['@name']] = buf
            return commit

        if 'project' not in diff['manifest']:
            return None
        buf = {}
        for key, val in diff['manifest']['project'].items():
            if str(key) == '$'+Diff.INSERT:
                for item in val:
                    index, _ = item
                    buf = _helper(data, data['manifest']['project'][int(index)], buf, label)
            elif '@name' in val:
                buf = _helper(data, data['manifest']['project'][int(key)], buf, label)
        return buf

    def _changed(self, data1, diff21, data2, diff12):
        def _default(data, diff, commit):
            for key, val in diff['manifest']['default'].items():
                if str(key) == '$'+Diff.DELETE or str(key) == '$'+Diff.INSERT:
                    continue
                if key == '@revision':
                    project = data['manifest']['project']
                    for item in project:
                        buf = commit.get(item['@name'], [])
                        buf.append({
                            Repo.BRANCH: item.get('@upstream', self._revision(data)),
                            Repo.COMMIT: item.get('@revision', '')
                        })
                        commit[item['@name']] = buf
            return commit

        def _project(data, diff, commit):
            for key, val in diff['manifest']['project'].items():
                if str(key) == '$'+Diff.DELETE or str(key) == '$'+Diff.INSERT:
                    continue
                if '@name' not in val and ('@revision' in val or '@upstream' in val):
                    project = data['manifest']['project'][int(key)]
                    buf = commit.get(project['@name'], [])
                    buf.append({
                        Repo.BRANCH: project.get('@upstream', self._revision(data)),
                        Repo.COMMIT: project.get('@revision', '')
                    })
                    commit[project['@name']] = buf
            return commit

        buf = {}
        if 'default' in diff21['manifest'] and 'default' in diff12['manifest']:
            buf = _default(data2, diff12, _default(data1, diff21, buf))
        elif 'project' in diff21['manifest'] and 'project' in diff12['manifest']:
            buf = _project(data2, diff12, _project(data1, diff21, buf))
        return buf

    def _deleted(self, data, diff):
        return self._commit(data, diff, Diff.DELETE)

    def _inserted(self, data, diff):
        return self._commit(data, diff, Diff.INSERT)

    def run(self, data1, data2):
        diff12 = jsondiff.diff(data1, data2)
        diff21 = jsondiff.diff(data2, data1)
        if len(diff12) == 0 or len(diff21) == 0:
            return {}
        if 'manifest' not in diff12 or 'manifest' not in diff21:
            raise DifferException('manifest invalid')
        return {
            Diff.CHANGE: self._changed(data1, diff21, data2, diff12),
            Diff.DELETE: self._deleted(data1, diff21),
            Diff.INSERT: self._inserted(data2, diff12)
        }
