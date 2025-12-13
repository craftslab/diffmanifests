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
            Commit.AUTHOR: 'David\bAnderson <dvander@google.com>',
            Commit.BRANCH: 'master',
            Commit.COMMIT: 'ab9c7e6d04c896ddcbfc2e3bc99ab00e6a892288',
            Commit.DATE: 'Tue Feb 18 23:29:44 2020 -0800',
            Commit.DIFF: Label.ADD_COMMIT.upper(),
            Commit.MESSAGE: 'Exclude holes from the block map.',
            Commit.REPO: 'platform/build',
            Commit.URL: 'https://android.googlesource.com/platform/build/+/ab9c7e6d04c896ddcbfc2e3bc99ab00e6a892288',
            Commit.CHANGE: 'https://android-review.googlesource.com/1000000',
            Commit.COMMITTER: 'David Anderson <dvander@google.com>',
            Commit.TOPIC: 'build'
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


def test_printer_with_special_characters():
    """Test printer with special characters in data"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    printer = Printer(config)
    assert printer is not None

    buf = [
        {
            Commit.AUTHOR: 'José García <jose@example.com>',
            Commit.BRANCH: 'master',
            Commit.COMMIT: 'ab9c7e6d04c896ddcbfc2e3bc99ab00e6a892288',
            Commit.DATE: 'Tue Feb 18 23:29:44 2020 -0800',
            Commit.DIFF: Label.ADD_COMMIT.upper(),
            Commit.MESSAGE: 'Add support for internationalization',
            Commit.REPO: 'platform/build',
            Commit.URL: 'https://android.googlesource.com/platform/build/+/ab9c7e6d04c896ddcbfc2e3bc99ab00e6a892288',
            Commit.CHANGE: 'https://android-review.googlesource.com/1000000',
            Commit.COMMITTER: 'José García <jose@example.com>',
            Commit.TOPIC: 'feature/internationalization'
        }
    ]

    name = 'output_special.json'
    printer.run(buf, name)
    assert os.path.isfile(name)
    os.remove(name)


def test_printer_empty_list():
    """Test printer with empty list"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    printer = Printer(config)
    assert printer is not None

    buf = []

    name = 'output_empty.json'
    printer.run(buf, name)
    assert os.path.isfile(name)
    os.remove(name)


def test_printer_multiple_entries():
    """Test printer with multiple entries"""
    config = load(os.path.join(os.path.dirname(__file__), '../../diffmanifests/config/config.json'))

    printer = Printer(config)
    assert printer is not None

    buf = [
        {
            Commit.AUTHOR: 'Author One <author1@example.com>',
            Commit.BRANCH: 'master',
            Commit.COMMIT: 'commit1hash',
            Commit.DATE: 'Tue Feb 18 23:29:44 2020 -0800',
            Commit.DIFF: Label.ADD_COMMIT.upper(),
            Commit.MESSAGE: 'First commit',
            Commit.REPO: 'platform/build',
            Commit.URL: 'https://android.googlesource.com/platform/build/+/commit1hash',
            Commit.CHANGE: 'https://android-review.googlesource.com/1000001',
            Commit.COMMITTER: 'Author One <author1@example.com>',
            Commit.TOPIC: 'topic1'
        },
        {
            Commit.AUTHOR: 'Author Two <author2@example.com>',
            Commit.BRANCH: 'develop',
            Commit.COMMIT: 'commit2hash',
            Commit.DATE: 'Wed Feb 19 10:00:00 2020 -0800',
            Commit.DIFF: Label.REMOVE_COMMIT.upper(),
            Commit.MESSAGE: 'Second commit',
            Commit.REPO: 'platform/build/kati',
            Commit.URL: 'https://android.googlesource.com/platform/build/kati/+/commit2hash',
            Commit.CHANGE: 'https://android-review.googlesource.com/1000002',
            Commit.COMMITTER: 'Author Two <author2@example.com>',
            Commit.TOPIC: 'topic2'
        }
    ]

    name = 'output_multiple.json'
    printer.run(buf, name)
    assert os.path.isfile(name)
    os.remove(name)


def test_printer_format_method():
    """Test that Printer.format() returns list of supported formats"""
    formats = Printer.format()
    assert isinstance(formats, list)
    assert len(formats) > 0
    assert '.json' in formats
    assert '.txt' in formats
    assert '.xlsx' in formats
