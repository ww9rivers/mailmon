#!/usr/bin/env python
##
## Module to extract and save attachments in mail messages.
##

from __future__ import print_function
import json
import os, re
from FileMonitor import FileMonitor
from c9r.pylog import logger
from c9r.html.text import Parser
from c9r.mail.parser import parse_date


class LogJson(FileMonitor):
    '''A MailMonitor module for extracting attachments.

    This module inherits configuration from FileMonitor.
    '''
    def __call__(self, msg):
        '''Extract attachment(s) in a given email message that has already
        been parsed and save them to a folder as configured.

        Keep time stamps on the attachments, using part.mod_date (mtime)
        and part.read_date (atime).
        '''
        body = msg['body']
        if not body:
            html = msg['html']
            if html: body = Parser(html).text()
        with open(self.routate_filename(self.config('output')), "wb") as outf:
            print(json.dumps({
                        '_time': parse_date(msg),
                        'received': [{'by': x['by'], 'time': x['time']} for x in msg['received']],
                        'text': msg['body'].strip()
                        }), file=self.outf)

    def __init__(self, conf):
        '''
        Configure this object, and open the output file.
        '''
        FileMonitor.__init__(self, conf)
        self.outf = open(self.routate_filename(self.config('output')), "a")


if __name__ == '__main__':
    import doctest
    doctest.testfile('test/LogBody.text')
