# -*- coding: utf-8 -*-

from ..proto.proto import Label, Repo


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
        if '@revision' not in data['manifest']['default']:
            return ''
        return data['manifest']['default']['@revision']

    def _diff(self, data1, data2):
        def _helper(data, project, name):
            revision = ''
            upstream = ''
            for item in project:
                if item['@name'] == name:
                    revision = item.get('@revision', '')
                    upstream = item.get('@upstream', self._revision(data))
                    break
            return revision, upstream

        project1 = data1['manifest']['project']
        if type(project1) is not list:
            project1 = [project1]

        name1 = []
        for item in project1:
            name1.append(item['@name'])

        project2 = data2['manifest']['project']
        if type(project2) is not list:
            project2 = [project2]

        name2 = []
        for item in project2:
            name2.append(item['@name'])

        added = {}
        buf = list(set(name2).difference(set(name1)))
        for item in buf:
            revision2, upstream2 = _helper(data2, project2, item)
            added[item] = [
                {},
                {
                    Repo.BRANCH: upstream2,
                    Repo.COMMIT: revision2
                }
            ]

        removed = {}
        buf = list(set(name1).difference(set(name2)))
        for item in buf:
            revision1, upstream1 = _helper(data1, project1, item)
            removed[item] = [
                {
                    Repo.BRANCH: upstream1,
                    Repo.COMMIT: revision1
                },
                {}
            ]

        updated = {}
        buf = list(set(name1).intersection(set(name2)))
        for item in buf:
            revision1, upstream1 = _helper(data1, project1, item)
            revision2, upstream2 = _helper(data2, project2, item)
            updated[item] = [
                {
                    Repo.BRANCH: upstream1,
                    Repo.COMMIT: revision1
                },
                {
                    Repo.BRANCH: upstream2,
                    Repo.COMMIT: revision2
                }
            ]

        return added, removed, updated

    def run(self, data1, data2):
        if 'manifest' not in data1 or 'manifest' not in data2:
            raise DifferException('manifest invalid')

        if 'default' not in data1['manifest'] or 'default' not in data2['manifest']:
            raise DifferException('default invalid')

        if 'project' not in data1['manifest'] or 'project' not in data2['manifest']:
            raise DifferException('project invalid')

        if 'remote' not in data1['manifest'] or 'remote' not in data2['manifest']:
            raise DifferException('remote invalid')

        added, removed, updated = self._diff(data1, data2)

        return {
            Label.ADD_REPO: added,
            Label.REMOVE_REPO: removed,
            Label.UPDATE_REPO: updated
        }
