#!/usr/bin/env python
#
## $Id: Extract.py,v 1.5 2015/06/11 21:39:48 weiwang Exp $
##
## Class for modules that need to deal with file(s) in email.

import os, re, time
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

    def output_filename(self, fname):
        '''Create an output filename with configured "path" and given "fname",
        as well as optionally configured regex-based fix on the file name.
        '''
        return fname if os.path.isabs(fname) else\
            os.path.join(self.path, fn if self.fix_name is None else\
                             '-'.join(self.fix_name.split(fn)))

    def routate_filename(self, fntemp):
        '''Create a fixed output filename, with a given template "fntemp",
        with current time applied, to allow automatic file rotation.
        '''
        return time.strftime(self.output_filename(fntemp))

    def __init__(self, conf):
        '''
        Configure this object.
        '''
        MailMonitor.__init__(self, conf)
        path = os.path.dirname(conf.get('output') or '')
        self.path = path = conf.get('path') or path or '/var/log/mailmon'
        if not os.path.isdir(path):
            forge_path(path)
        self.to_print = conf.get('print-name', False)
        self.fix_name = None if not conf.get('fix-name', True)\
            else re.compile('[^\w\d_\-\.]')
        logger.info("%s: path = %s" % (type(self).__name__, path))
