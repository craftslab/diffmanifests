# -*- coding: utf-8 -*-

import os

from diffmanifests.main import load
from diffmanifests.printer.printer import Printer, PrinterException
from diffmanifests.proto.proto import Commit, Label


def test_exception():
    exception = PrinterException('exception')
    assert str(exception) == 'exception'


def test_printer():
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    printer = Printer(config)
    assert printer is not None

    buf = [
        {
            Commit.AUTHOR: 'David Anderson <dvander@google.com>',
            Commit.BRANCH: 'master',
            Commit.COMMIT: 'ab9c7e6d04c896ddcbfc2e3bc99ab00e6a892288',
            Commit.DATE: 'Tue Feb 18 23:29:44 2020 -0800',
            Commit.DIFF: Label.ADD_COMMIT.upper(),
            Commit.MESSAGE: 'Exclude holes from the block map.',
            Commit.REPO: 'platform/build',
            Commit.URL: 'https://android.googlesource.com/platform/build/+/ab9c7e6d04c896ddcbfc2e3bc99ab00e6a892288'
        }
    ]

    name = 'output.json'
    printer.run(buf, name)
    assert os.path.isfile(name)
    os.remove(name)

    name = 'output.txt'
    printer.run(buf, name)
    assert os.path.isfile(name)
    os.remove(name)

    name = 'output.xlsx'
    printer.run(buf, name)
    assert os.path.isfile(name)
    os.remove(name)
