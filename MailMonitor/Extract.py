#!/usr/bin/env python
#
## $Id: Extract.py,v 1.5 2015/06/11 21:39:48 weiwang Exp $
##
## Module to extract and save attachments in mail messages.

import os, re
from MailMonitor import MailMonitor
from c9r.pylog import logger
from c9r.file.util import forge_path
from c9r.mail.parser import parse_date


class Extract(MailMonitor):
    '''A MailMonitor module for extracting attachments.

    This module look for these configuration items in a mailmonitor job:

      fix-name          Defaults to True, to convert any character other than
                        [\w\d_\-\.] in attachment file names to hyphen ("-").
      path              Path to a folder to save extracted files.
      print-name        Print out names of the files extracted.

    '''
    def __call__(self, msg):
        '''Extract attachment(s) in a given email message that has already
        been parsed and save them to a folder as configured.

        Keep time stamps on the attachments, using part.mod_date (mtime)
        and part.read_date (atime).
        '''
        mtime = parse_date(msg)
        for part in msg['attachments']:
            fn = part.name
            outfname = os.path.join(self.path,
                                    fn if self.fix_name is None\
                                        else '-'.join(self.fix_name.split(fn)))
            with open(outfname, "wb") as outf:
                outf.write(part.read(part.size))
            os.utime(outfname, (getattr(part, 'atime', mtime), getattr(part, 'mtime', mtime)))
            if self.to_print:
                print(outfname)
            logger.info("Extracted attachment '%s'"%(outfname))

    def __init__(self, conf):
        '''
        Configure this object.
        '''
        MailMonitor.__init__(self, conf)
        self.path = path = conf.get('path', '/var/log/mailmon')
        if not os.path.isdir(path):
            forge_path(path)
        self.to_print = conf.get('print-name', False)
        self.fix_name = None if not conf.get('fix-name', True)\
            else re.compile('[^\w\d_\-\.]')
        logger.info("Extract: path = %s" % (path))

if __name__ == '__main__':
    import doctest
    doctest.testfile('test/Extract.text')