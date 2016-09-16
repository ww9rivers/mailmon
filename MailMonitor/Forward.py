#!/usr/bin/env python
#
## $Id: Forward.py,v 1.2 2014/07/14 12:15:18 weiwang Exp $
##
## Module to extract and save attachments in mail messages.

import os
from MailMonitor import MailMonitor
from c9r.pylog import logger


class Forward(MailMonitor):
    '''
    A MailMonitor for extracting attachments.
    '''
    def __call__(self, msg):
        xc = self.CONF.smtp
        try:
            self.smtp = smtplib.SMTP(xc.server, xc.port)
            raise Exception('MailMonitor.Forward is not completed yet.')
        except Exception as xerr:
            logger.error('Failed to connect SMTP server for sending email: %s' % (xerr))
            return -2

    def __init__(self, conf):
        '''
        Configure this object.
        '''
        MailMonitor.__init__(self, conf)
