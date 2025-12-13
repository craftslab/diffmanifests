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
