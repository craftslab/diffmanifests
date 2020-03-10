# -*- coding: utf-8 -*-

from diffmanifests.cmd.argument import Argument


def test_argument():
    argument = Argument()
    assert argument is not None
