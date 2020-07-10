# -*- coding: utf-8 -*-

import json
import openpyxl
import os
import time

from ..proto.proto import Commit

head = {
    'A': Commit.DIFF,
    'B': Commit.REPO,
    'C': Commit.BRANCH,
    'D': Commit.AUTHOR,
    'E': Commit.DATE,
    'F': Commit.COMMIT,
    'G': Commit.MESSAGE,
    'H': Commit.URL
}


class PrinterException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Printer(object):
    _format = ['.json', '.txt', '.xlsx']

    def __init__(self, config=None):
        if config is None:
            pass

    @staticmethod
    def format():
        return Printer._format

    def _json(self, data, name):
        with open(name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))

    def _txt(self, data, name):
        def _txt_helper(data, out):
            global head
            out.write(u'%s%s: %s\n' % (' '*3, head['A'], data[head['A']]))
            out.write(u'%s%s: %s\n' % (' '*3, head['B'], data[head['B']]))
            out.write(u'%s%s: %s\n' % (' '*1, head['C'], data[head['C']]))
            out.write(u'%s%s: %s\n' % (' '*1, head['D'], data[head['D']]))
            out.write(u'%s%s: %s\n' % (' '*3, head['E'], data[head['E']]))
            out.write(u'%s%s: %s\n' % (' '*1, head['F'], data[head['F']]))
            out.write(u'%s%s: %s\n' % (' '*0, head['G'], data[head['G']]))
            out.write(u'%s%s: %s\n' % (' '*0, head['H'], data[head['H']]))
            out.write('\n')

        with open(name, 'w', encoding='utf8') as f:
            f.write('')
            for item in data:
                _txt_helper(item, f)

    def _xlsx(self, data, name):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        ws.append([head[key].upper() for key in sorted(head.keys())])
        for item in data:
            ws.append([item[head[key]] for key in sorted(head.keys())])
        wb.save(filename=name)

    def run(self, data, name):
        func = Printer.__dict__.get(os.path.splitext(name)[1].replace('.', '_'), None)
        if func is not None:
            func(self, data, name)
