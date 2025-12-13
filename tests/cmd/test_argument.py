# -*- coding: utf-8 -*-

import sys
from diffmanifests.cmd.argument import Argument


def test_argument():
    argument = Argument()
    assert argument is not None


def test_argument_parse_required_args():
    """Test that parse correctly processes required arguments"""
    argument = Argument()
    args = argument.parse([
        'prog',
        '-c', 'config.json',
        '-m', 'manifest1.xml',
        '-n', 'manifest2.xml',
        '-o', 'output.json'
    ])

    assert args.config_file == 'config.json'
    assert args.manifest1_file == 'manifest1.xml'
    assert args.manifest2_file == 'manifest2.xml'
    assert args.output_file == 'output.json'


def test_argument_parse_with_optional_args():
    """Test that parse correctly processes optional arguments"""
    argument = Argument()
    args = argument.parse([
        'prog',
        '-c', 'config.json',
        '-m', 'manifest1.xml',
        '-n', 'manifest2.xml',
        '-o', 'output.json',
        '-r', '3000'
    ])

    assert args.recursion_depth == 3000


def test_argument_parse_default_recursion_depth():
    """Test that default recursion depth is applied"""
    argument = Argument()
    args = argument.parse([
        'prog',
        '-c', 'config.json',
        '-m', 'manifest1.xml',
        '-n', 'manifest2.xml',
        '-o', 'output.json'
    ])

    assert args.recursion_depth == 2000


def test_argument_parse_long_form_args():
    """Test that long form arguments work correctly"""
    argument = Argument()
    args = argument.parse([
        'prog',
        '--config-file', 'config.json',
        '--manifest1-file', 'manifest1.xml',
        '--manifest2-file', 'manifest2.xml',
        '--output-file', 'output.json',
        '--recursion-depth', '5000'
    ])

    assert args.config_file == 'config.json'
    assert args.manifest1_file == 'manifest1.xml'
    assert args.manifest2_file == 'manifest2.xml'
    assert args.output_file == 'output.json'
    assert args.recursion_depth == 5000
