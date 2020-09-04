# -*- coding: utf-8 -*-

import argparse

from ..printer.printer import Printer
from .version import VERSION


class Argument(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description='Diff Manifests')
        self._add()

    def _add(self):
        self._parser.add_argument('-c', '--config-file',
                                  dest='config_file',
                                  help='config file, format: .json',
                                  required=True)
        self._parser.add_argument('-m', '--manifest1-file',
                                  dest='manifest1_file',
                                  help='manifest1 file, format: .xml',
                                  required=True)
        self._parser.add_argument('-n', '--manifest2-file',
                                  dest='manifest2_file',
                                  help='manifest2 file, format: .xml',
                                  required=True)
        self._parser.add_argument('-o', '--output-file',
                                  dest='output_file',
                                  help='output file, format: ' + ', '.join(Printer.format()),
                                  required=True)
        self._parser.add_argument('-r', '--recursion-depth',
                                  default=2000,
                                  dest='recursion_depth',
                                  help='recursion depth',
                                  type=int)
        self._parser.add_argument('-v', '--version',
                                  action='version',
                                  version=VERSION)

    def parse(self, argv):
        return self._parser.parse_args(argv[1:])
