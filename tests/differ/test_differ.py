# -*- coding: utf-8 -*-

import os
import pprint

from diffmanifests.differ.differ import Differ, DifferException
from diffmanifests.main import load


def test_exception():
    exception = DifferException('exception')
    assert str(exception) == 'exception'


def test_differ():
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    differ = Differ(config)
    assert differ is not None

    path = os.path.join(os.path.dirname(__file__), '../data')
    files = os.listdir(path)

    for index in range(0, len(files)//2):
        data1 = load(os.path.join(path, 'manifest1-%s.xml' % format(index+1, '003')))
        data2 = load(os.path.join(path, 'manifest2-%s.xml' % format(index+1, '003')))

        buf = differ.run(data1, data2)
        assert buf is not None
        pprint.pprint(buf)


def test_differ_duplicate_names():
    """Test differ with duplicated 'name' but different 'upstream'."""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    differ = Differ(config)
    assert differ is not None

    path = os.path.join(os.path.dirname(__file__), '../data')

    # Load manifest1-004.xml and manifest2-004.xml
    data1 = load(os.path.join(path, 'manifest1-004.xml'))
    data2 = load(os.path.join(path, 'manifest2-004.xml'))

    buf = differ.run(data1, data2)
    assert buf is not None

    print("\n=== Test: Duplicate names with different upstream ===")
    pprint.pprint(buf)

    # Verify that we can distinguish between the two projects
    # Both should appear in the 'update repo' section
    assert 'update repo' in buf
    updated = buf['update repo']

    # Should have 2 entries (one for main, one for android16-release)
    assert len(updated) == 2

    # Check that both upstream branches are present
    upstreams = set()
    for key, value in updated.items():
        old_branch = value[0]['branch']
        new_branch = value[1]['branch']
        assert old_branch == new_branch  # Same branch in both manifests
        upstreams.add(old_branch)

    # Should have both 'main' and 'android16-release'
    assert 'main' in upstreams
    assert 'android16-release' in upstreams

    print("✓ Test passed: Successfully differentiated projects with same name but different upstream")


def test_differ_with_none_config():
    """Test differ initialization with None config"""
    differ = Differ(None)
    assert differ is not None


def test_differ_revision_empty():
    """Test _revision returns empty string when @revision is missing"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    differ = Differ(config)

    data = {
        'manifest': {
            'default': {}
        }
    }

    revision = differ._revision(data)
    assert revision == ''


def test_differ_with_identical_manifests():
    """Test differ with identical manifests returns empty diffs"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    differ = Differ(config)

    path = os.path.join(os.path.dirname(__file__), '../data')
    data = load(os.path.join(path, 'manifest1-001.xml'))

    buf = differ.run(data, data)
    assert buf is not None

    # All sections should be empty
    assert len(buf['add repo']) == 0
    assert len(buf['remove repo']) == 0
    assert len(buf['update repo']) == 0


def test_differ_with_single_project():
    """Test differ correctly handles single project (not list)"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    differ = Differ(config)

    # Create manifest with single project (not list)
    data1 = {
        'manifest': {
            'default': {'@revision': 'master'},
            'remote': [{'@name': 'origin'}],
            'project': {
                '@name': 'platform/build',
                '@revision': 'abc123'
            }
        }
    }

    data2 = {
        'manifest': {
            'default': {'@revision': 'master'},
            'remote': [{'@name': 'origin'}],
            'project': {
                '@name': 'platform/build',
                '@revision': 'def456'
            }
        }
    }

    buf = differ.run(data1, data2)
    assert buf is not None
    assert len(buf['update repo']) == 1


def test_differ_missing_manifest_key():
    """Test differ raises exception when manifest key is missing"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    differ = Differ(config)

    data1 = {'no_manifest': {}}
    data2 = {'manifest': {}}

    try:
        differ.run(data1, data2)
        assert False, "Should raise DifferException"
    except Exception as e:
        assert 'manifest invalid' in str(e)


def test_differ_missing_default_key():
    """Test differ raises exception when default key is missing"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    differ = Differ(config)

    data1 = {'manifest': {'default': {}, 'project': [], 'remote': []}}
    data2 = {'manifest': {'project': [], 'remote': []}}

    try:
        differ.run(data1, data2)
        assert False, "Should raise DifferException"
    except Exception as e:
        assert 'default invalid' in str(e)


def test_differ_missing_project_key():
    """Test differ raises exception when project key is missing"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    differ = Differ(config)

    data1 = {'manifest': {'default': {}, 'project': [], 'remote': []}}
    data2 = {'manifest': {'default': {}, 'remote': []}}

    try:
        differ.run(data1, data2)
        assert False, "Should raise DifferException"
    except Exception as e:
        assert 'project invalid' in str(e)


def test_differ_missing_remote_key():
    """Test differ raises exception when remote key is missing"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))
    differ = Differ(config)

    data1 = {'manifest': {'default': {}, 'project': [], 'remote': []}}
    data2 = {'manifest': {'default': {}, 'project': []}}

    try:
        differ.run(data1, data2)
        assert False, "Should raise DifferException"
    except Exception as e:
        assert 'remote invalid' in str(e)
