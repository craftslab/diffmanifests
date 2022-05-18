# -*- coding: utf-8 -*-

import json
import openpyxl
import os
import re
import time

from openpyxl.styles import Alignment, Font
from ..proto.proto import Commit

# Refer: openpyxl/cell/cell.py
ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

head = {
    'A': Commit.DIFF,
    'B': Commit.REPO,
    'C': Commit.BRANCH,
    'D': Commit.AUTHOR,
    'E': Commit.DATE,
    'F': Commit.COMMIT,
    'G': Commit.MESSAGE,
    'H': Commit.URL,
    'I': Commit.CHANGE,
    'J': Commit.COMMITTER,
    'K': Commit.TOPIC
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
            out.write(u'%s%s: %s\n' % (' '*5, head['A'], data[head['A']]))
            out.write(u'%s%s: %s\n' % (' '*5, head['B'], data[head['B']]))
            out.write(u'%s%s: %s\n' % (' '*3, head['C'], data[head['C']]))
            out.write(u'%s%s: %s\n' % (' '*3, head['D'], data[head['D']]))
            out.write(u'%s%s: %s\n' % (' '*5, head['E'], data[head['E']]))
            out.write(u'%s%s: %s\n' % (' '*3, head['F'], data[head['F']]))
            out.write(u'%s%s: %s\n' % (' '*2, head['G'], data[head['G']]))
            out.write(u'%s%s: %s\n' % (' '*6, head['H'], data[head['H']]))
            out.write(u'%s%s: %s\n' % (' '*3, head['I'], data[head['I']]))
            out.write(u'%s%s: %s\n' % (' '*0, head['J'], data[head['J']]))
            out.write(u'%s%s: %s\n' % (' '*4, head['K'], data[head['K']]))
            out.write('\n')

        with open(name, 'w', encoding='utf8') as f:
            f.write('')
            for item in data:
                _txt_helper(item, f)

    def _xlsx(self, data, name):
        def _styling_head(sheet):
            for item in head.keys():
                sheet[item+'1'].alignment = Alignment(horizontal='center', shrink_to_fit=True, vertical='center')
                sheet[item+'1'].font = Font(bold=True, name='Calibri')
            sheet.freeze_panes = sheet['B2']

        def _styling_data(sheet, rows):
            for key in head.keys():
                for row in range(rows):
                    sheet[key+str(row+2)].alignment = Alignment(vertical='center')
                    sheet[key+str(row+2)].font = Font(bold=False, name='Calibri')

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        ws.append([head[key].upper() for key in sorted(head.keys())])
        for item in data:
            buf = []
            for key in sorted(head.keys()):
                buf.append(re.sub(ILLEGAL_CHARACTERS_RE, ' ', item[head[key]]))
            ws.append(buf)
        _styling_head(ws)
        _styling_data(ws, len(data))
        wb.save(filename=name)

    def run(self, data, name):
        func = Printer.__dict__.get(os.path.splitext(name)[1].replace('.', '_'), None)
        if func is not None:
            func(self, data, name)
