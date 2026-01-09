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
        def _make_key(item):
            # Use path if available to uniquely identify the project across branch/upstream changes
            return item.get('@path', item['@name'])

        def _helper(data, project, key):
            revision = ''
            upstream = ''
            name = ''
            for item in project:
                item_name = item['@name']
                item_upstream = item.get('@upstream', self._revision(data))
                item_key = _make_key(item)
                if item_key == key:
                    revision = item.get('@revision', '')
                    upstream = item_upstream
                    name = item_name
                    break
            return name, revision, upstream

        project1 = data1['manifest']['project']
        if type(project1) is not list:
            project1 = [project1]

        # Default revisions are kept for display only; matching ignores upstream changes
        default_revision1 = self._revision(data1)
        keys1 = []
        for item in project1:
            keys1.append(_make_key(item))

        project2 = data2['manifest']['project']
        if type(project2) is not list:
            project2 = [project2]

        default_revision2 = self._revision(data2)
        keys2 = []
        for item in project2:
            keys2.append(_make_key(item))

        added = {}
        buf = list(set(keys2).difference(set(keys1)))
        for key in buf:
            name, revision2, upstream2 = _helper(data2, project2, key)
            # Use path/name as display key to differentiate duplicates with different paths
            display_key = key
            added[display_key] = [
                {},
                {
                    Repo.NAME: name,
                    Repo.BRANCH: upstream2,
                    Repo.COMMIT: revision2
                }
            ]

        removed = {}
        buf = list(set(keys1).difference(set(keys2)))
        for key in buf:
            name, revision1, upstream1 = _helper(data1, project1, key)
            # Use path/name as display key to differentiate duplicates with different paths
            display_key = key
            removed[display_key] = [
                {
                    Repo.NAME: name,
                    Repo.BRANCH: upstream1,
                    Repo.COMMIT: revision1
                },
                {}
            ]

        updated = {}
        buf = list(set(keys1).intersection(set(keys2)))
        for key in buf:
            name1, revision1, upstream1 = _helper(data1, project1, key)
            name2, revision2, upstream2 = _helper(data2, project2, key)
            if revision1 == revision2:
                continue
            # Use path/name as display key to differentiate duplicates with different paths
            display_key = key
            updated[display_key] = [
                {
                    Repo.NAME: name1,
                    Repo.BRANCH: upstream1,
                    Repo.COMMIT: revision1
                },
                {
                    Repo.NAME: name2,
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
