# -*- coding: utf-8 -*-

import json
import os
import sys
import xmltodict

from .cmd.argument import Argument
from .cmd.banner import BANNER
from .differ.differ import Differ, DifferException
from .logger.logger import Logger
from .printer.printer import Printer, PrinterException
from .querier.querier import Querier, QuerierException


def load(name):
    with open(name, 'r') as f:
        if name.endswith('.json'):
            data = json.load(f)
        elif name.endswith('.xml'):
            data = json.loads(json.dumps(xmltodict.parse(f.read())))
        else:
            data = None
    return data


def main():
    print(BANNER)

    argument = Argument()
    arg = argument.parse(sys.argv)

    if os.path.exists(arg.config_file) and arg.config_file.endswith('.json'):
        config = load(arg.config_file)
    else:
        Logger.error('config invalid: %s' % arg.config_file)
        return -1

    if os.path.exists(arg.manifest1_file) and arg.manifest1_file.endswith('.xml'):
        manifest1 = load(arg.manifest1_file)
    else:
        Logger.error('manifest invalid: %s' % arg.manifest1_file)
        return -2

    if os.path.exists(arg.manifest2_file) and arg.manifest2_file.endswith('.xml'):
        manifest2 = load(arg.manifest2_file)
    else:
        Logger.error('manifest invalid: %s' % arg.manifest2_file)
        return -3

    if os.path.exists(arg.output_file) or os.path.splitext(arg.output_file)[1] not in Printer.format():
        Logger.error('output invalid: %s' % arg.output_file)
        return -4

    sys.setrecursionlimit(arg.recursion_depth)

    try:
        differ = Differ(config)
        buf = differ.run(manifest1, manifest2)
    except DifferException as e:
        Logger.error(str(e))
        return -5

    if len(buf) == 0:
        Logger.info('manifest identical')
        return 0

    try:
        querier = Querier(config)
        buf = querier.run(buf)
    except QuerierException as e:
        Logger.error(str(e))
        return -6

    try:
        printer = Printer(config)
        printer.run(buf, arg.output_file)
    except PrinterException as e:
        Logger.error(str(e))
        return -7

    return 0
