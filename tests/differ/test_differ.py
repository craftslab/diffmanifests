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
