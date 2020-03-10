# -*- coding: utf-8 -*-

import colorama
import sys
import time


class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def debug(msg):
        sys.stderr.write(u'{debug}{time} DEBUG:{reset} {msg}\n'.format(
            debug=colorama.Fore.GREEN + colorama.Style.BRIGHT,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            reset=colorama.Style.RESET_ALL,
            msg=msg))

    @staticmethod
    def error(msg):
        sys.stderr.write(u'{error}{time} ERROR:{reset} {msg}\n'.format(
            error=colorama.Fore.RED + colorama.Style.BRIGHT,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            reset=colorama.Style.RESET_ALL,
            msg=msg))

    @staticmethod
    def info(msg):
        sys.stderr.write(u'{info}{time} INFO:{reset} {msg}\n'.format(
            info=colorama.Fore.WHITE + colorama.Style.BRIGHT,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            reset=colorama.Style.RESET_ALL,
            msg=msg))

    @staticmethod
    def warn(msg):
        sys.stderr.write(u'{warn}{time} WARN:{reset} {msg}\n'.format(
            warn=colorama.Fore.YELLOW + colorama.Style.BRIGHT,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            reset=colorama.Style.RESET_ALL,
            msg=msg))
