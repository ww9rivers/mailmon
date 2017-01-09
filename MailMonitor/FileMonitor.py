#!/usr/bin/env python
#
## $Id: Extract.py,v 1.5 2015/06/11 21:39:48 weiwang Exp $
##
## Class for modules that need to deal with file(s) in email.

import os, re
from MailMonitor import MailMonitor
from c9r.pylog import logger
from c9r.file.util import forge_path


class FileMonitor(MailMonitor):
    '''A MailMonitor module for extracting attachments.

    This module look for these configuration items in a mailmonitor job:

      fix-name          Defaults to True, to convert any character other than
                        [\w\d_\-\.] in attachment file names to hyphen ("-").
      path              Path to a folder to save extracted files.
      print-name        Print out names of the files extracted.

    '''
    def display(self, fname):
        ''' Print the given file name, if so configured.
        '''
        if self.to_print: print(fname)

    def __init__(self, conf):
        '''
        Configure this object.
        '''
        MailMonitor.__init__(self, conf)
        self.path = path = conf.get('path') or '/var/log/mailmon'
        if not os.path.isdir(path):
            forge_path(path)
        self.to_print = conf.get('print-name', False)
        self.fix_name = None if not conf.get('fix-name', True)\
            else re.compile('[^\w\d_\-\.]')
        logger.info("%s: path = %s" % (type(self).__name__, path))
