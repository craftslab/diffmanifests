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
        manifest1 = load(os.path.join(path, 'manifest1-%s.xml' % format(index+1, '003')))
        manifest2 = load(os.path.join(path, 'manifest2-%s.xml' % format(index+1, '003')))

        buf = differ.run(manifest1, manifest2)
        assert buf is not None
        pprint.pprint(buf)
