# -*- coding: utf-8 -*-

import os
import json
import tempfile
import unittest.mock

from diffmanifests.main import load, main


def test_load_json():
    """Test loading a JSON file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({'test': 'data'}, f)
        f.flush()
        temp_file = f.name

    try:
        data = load(temp_file)
        assert data is not None
        assert data['test'] == 'data'
    finally:
        os.remove(temp_file)


def test_load_xml():
    """Test loading an XML file"""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <default revision="master"/>
    <project name="platform/build" path="build" revision="abc123"/>
</manifest>
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(xml_content)
        f.flush()
        temp_file = f.name

    try:
        data = load(temp_file)
        assert data is not None
        assert 'manifest' in data
    finally:
        os.remove(temp_file)


def test_load_invalid_extension():
    """Test loading a file with invalid extension"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('test')
        f.flush()
        temp_file = f.name

    try:
        data = load(temp_file)
        assert data is None
    finally:
        os.remove(temp_file)


def test_main_invalid_config():
    """Test main with invalid config file"""
    with unittest.mock.patch('sys.argv', [
        'diffmanifests',
        '-c', 'nonexistent.json',
        '-m', 'manifest1.xml',
        '-n', 'manifest2.xml',
        '-o', 'output.json'
    ]):
        result = main()
        assert result == -1


def test_main_invalid_manifest1():
    """Test main with invalid manifest1 file"""
    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'

    with unittest.mock.patch('sys.argv', [
        'diffmanifests',
        '-c', config_file,
        '-m', 'nonexistent.xml',
        '-n', 'manifest2.xml',
        '-o', 'output.json'
    ]):
        result = main()
        assert result == -2


def test_main_invalid_manifest2():
    """Test main with invalid manifest2 file"""
    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'

    with unittest.mock.patch('sys.argv', [
        'diffmanifests',
        '-c', config_file,
        '-m', manifest1_file,
        '-n', 'nonexistent.xml',
        '-o', 'output.json'
    ]):
        result = main()
        assert result == -3


def test_main_invalid_output():
    """Test main with invalid output file"""
    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'
    manifest2_file = '/workspaces/diffmanifests/tests/data/manifest2-001.xml'

    # Create a temporary file to represent existing output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{}')
        f.flush()
        output_file = f.name

    try:
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', manifest1_file,
            '-n', manifest2_file,
            '-o', output_file  # File already exists
        ]):
            result = main()
            assert result == -4
    finally:
        os.remove(output_file)


def test_main_success_flow():
    """Test main end-to-end success using mocks to avoid network calls."""
    import types
    from diffmanifests.differ.differ import Differ
    from diffmanifests.querier.querier import Querier
    from diffmanifests.printer.printer import Printer

    # Prepare temp manifests
    manifest1_xml = """<?xml version='1.0' encoding='utf-8'?>\n<manifest>\n  <remote name='zte' fetch='..'/>\n  <default revision='master' remote='zte'/>\n  <project name='platform/build' revision='abc123'/>\n</manifest>\n"""
    manifest2_xml = """<?xml version='1.0' encoding='utf-8'?>\n<manifest>\n  <remote name='zte' fetch='..'/>\n  <default revision='master' remote='zte'/>\n  <project name='platform/build' revision='def456'/>\n</manifest>\n"""

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f2:
        f1.write(manifest1_xml)
        f2.write(manifest2_xml)
        manifest1_file = f1.name
        manifest2_file = f2.name

    output_file = manifest1_file + '.xlsx'

    # Create a simple config file path
    config_file = os.path.join(os.path.dirname(__file__), '../diffmanifests/config/config.json')

    # Patch Differ, Querier, Printer to avoid external calls
    class MockDiffer:
        def __init__(self, *_):
            pass
        def run(self, *_):
            return {
                'update repo': {
                    'platform/build': [
                        {'name': 'platform/build', 'branch': 'master', 'commit': 'abc123'},
                        {'name': 'platform/build', 'branch': 'master', 'commit': 'def456'}
                    ]
                }
            }

    class MockQuerier:
        def __init__(self, *_):
            pass
        def run(self, buf):
            # Inject a minimal commit object to be printed
            return [
                {
                    'author': 'Test <test@example.com>',
                    'branch': 'master',
                    'change': '',
                    'commit': 'def456',
                    'committer': 'Test <test@example.com>',
                    'date': 'Mon Jan 01 00:00:00 2024 +0000',
                    'diff': 'ADD COMMIT',
                    'hashtags': [],
                    'message': 'Test message',
                    'repo': 'platform/build',
                    'topic': '',
                    'url': 'http://example.com/platform/build/+/def456'
                }
            ]

    class MockPrinter:
        _format = ['.json', '.txt', '.xlsx']

        def __init__(self, *_):
            pass

        def run(self, buf, name):
            # Write a minimal file to emulate output
            with open(name, 'wb') as f:
                f.write(b'OK')

        @staticmethod
        def format():
            return MockPrinter._format

    import unittest.mock
    with unittest.mock.patch('diffmanifests.main.Differ', MockDiffer), \
         unittest.mock.patch('diffmanifests.main.Querier', MockQuerier), \
         unittest.mock.patch('diffmanifests.main.Printer', MockPrinter), \
         unittest.mock.patch('sys.argv', [
             'diffmanifests',
             '-c', config_file,
             '-m', manifest1_file,
             '-n', manifest2_file,
             '-o', output_file
         ]):
        result = main()
        try:
            assert result == 0
            assert os.path.exists(output_file)
        finally:
            # Cleanup temp files
            os.remove(manifest1_file)
            os.remove(manifest2_file)
            if os.path.exists(output_file):
                os.remove(output_file)


def test_main_config_file_invalid_format():
    """Test main with config file in invalid format"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('test')
        f.flush()
        config_file = f.name

    try:
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', 'manifest1.xml',
            '-n', 'manifest2.xml',
            '-o', 'output.json'
        ]):
            result = main()
            assert result == -1
    finally:
        os.remove(config_file)


def test_main_manifest1_invalid_format():
    """Test main with manifest1 file in invalid format"""
    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('test')
        f.flush()
        manifest_file = f.name

    try:
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', manifest_file,
            '-n', 'manifest2.xml',
            '-o', 'output.json'
        ]):
            result = main()
            assert result == -2
    finally:
        os.remove(manifest_file)


def test_main_manifest2_invalid_format():
    """Test main with manifest2 file in invalid format"""
    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('test')
        f.flush()
        manifest_file = f.name

    try:
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', manifest1_file,
            '-n', manifest_file,
            '-o', 'output.json'
        ]):
            result = main()
            assert result == -3
    finally:
        os.remove(manifest_file)


def test_main_output_invalid_format():
    """Test main with output file in invalid format"""
    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'
    manifest2_file = '/workspaces/diffmanifests/tests/data/manifest2-001.xml'

    with unittest.mock.patch('sys.argv', [
        'diffmanifests',
        '-c', config_file,
        '-m', manifest1_file,
        '-n', manifest2_file,
        '-o', 'output.pdf'
    ]):
        result = main()
        assert result == -4


def test_main_differ_exception():
    """Test main with DifferException"""
    from diffmanifests.differ.differ import DifferException

    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'
    manifest2_file = '/workspaces/diffmanifests/tests/data/manifest2-001.xml'

    class MockDiffer:
        def __init__(self, *_):
            pass
        def run(self, *_):
            raise DifferException('Differ error')

    with unittest.mock.patch('diffmanifests.main.Differ', MockDiffer):
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', manifest1_file,
            '-n', manifest2_file,
            '-o', 'output.json'
        ]):
            result = main()
            assert result == -5


def test_main_querier_exception():
    """Test main with QuerierException"""
    from diffmanifests.querier.querier import QuerierException

    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'
    manifest2_file = '/workspaces/diffmanifests/tests/data/manifest2-001.xml'

    class MockDiffer:
        def __init__(self, *_):
            pass
        def run(self, *_):
            return {'update repo': {'test': [{'commit': 'abc'}, {'commit': 'def'}]}}

    class MockQuerier:
        def __init__(self, *_):
            pass
        def run(self, *_):
            raise QuerierException('Querier error')

    with unittest.mock.patch('diffmanifests.main.Differ', MockDiffer), \
         unittest.mock.patch('diffmanifests.main.Querier', MockQuerier):
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', manifest1_file,
            '-n', manifest2_file,
            '-o', 'output.json'
        ]):
            result = main()
            assert result == -6


def test_main_printer_exception():
    """Test main with PrinterException"""
    from diffmanifests.printer.printer import PrinterException

    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'
    manifest2_file = '/workspaces/diffmanifests/tests/data/manifest2-001.xml'

    class MockDiffer:
        def __init__(self, *_):
            pass
        def run(self, *_):
            return {'update repo': {'test': [{'commit': 'abc'}, {'commit': 'def'}]}}

    class MockQuerier:
        def __init__(self, *_):
            pass
        def run(self, buf):
            return [{
                'author': 'Test <test@example.com>',
                'branch': 'master',
                'change': '',
                'commit': 'def456',
                'committer': 'Test <test@example.com>',
                'date': 'Mon Jan 01 00:00:00 2024 +0000',
                'diff': 'ADD COMMIT',
                'hashtags': [],
                'message': 'Test message',
                'repo': 'platform/build',
                'topic': '',
                'url': 'http://example.com'
            }]

    class MockPrinter:
        _format = ['.json', '.txt', '.xlsx']

        def __init__(self, *_):
            pass

        def run(self, buf, name):
            raise PrinterException('Printer error')

        @staticmethod
        def format():
            return MockPrinter._format

    with unittest.mock.patch('diffmanifests.main.Differ', MockDiffer), \
         unittest.mock.patch('diffmanifests.main.Querier', MockQuerier), \
         unittest.mock.patch('diffmanifests.main.Printer', MockPrinter):
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', manifest1_file,
            '-n', manifest2_file,
            '-o', 'output.json'
        ]):
            result = main()
            assert result == -7


def test_main_output_file_exists():
    """Test main with output file that already exists"""
    config_file = '/workspaces/diffmanifests/diffmanifests/config/config.json'
    manifest1_file = '/workspaces/diffmanifests/tests/data/manifest1-001.xml'
    manifest2_file = '/workspaces/diffmanifests/tests/data/manifest2-001.xml'

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{}')
        f.flush()
        output_file = f.name

    try:
        with unittest.mock.patch('sys.argv', [
            'diffmanifests',
            '-c', config_file,
            '-m', manifest1_file,
            '-n', manifest2_file,
            '-o', output_file
        ]):
            result = main()
            assert result == -4
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)
