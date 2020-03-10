# -*- coding: utf-8 -*-

from diffmanifests.logger.logger import Logger


def test_debug(capsys):
    logger = Logger()
    logger.debug('debug')
    captured = capsys.readouterr()
    assert 'debug\n' in captured.err


def test_error(capsys):
    logger = Logger()
    logger.error('error')
    captured = capsys.readouterr()
    assert 'error\n' in captured.err


def test_info(capsys):
    logger = Logger()
    logger.info('info')
    captured = capsys.readouterr()
    assert 'info\n' in captured.err


def test_warn(capsys):
    logger = Logger()
    logger.warn('warn')
    captured = capsys.readouterr()
    assert 'warn\n' in captured.err
