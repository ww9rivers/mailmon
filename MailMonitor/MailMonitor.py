#!/usr/bin/env python
#
## $Id: MailMonitor.py,v 1.3 2014/07/14 12:15:18 weiwang Exp $
##
## Base module for email monitor plugins.

import datetime


class MailMonitor:
    '''
    Base plugin object for MailMonitorApp.
    '''
    def archive(self):
        '''
        Return the archive mailbox name for this task.
        '''
        return self.CONF.get('archive')

    def ignores_message(self, mbox, auid):
        '''
        Returns true if the message is irrelevant. This method allows a plugin
        an opportunity to work with the message id and mailbox before the
        MailMonitorApp retrieves the message.
        '''
        return False

    def mailbox(self):
        '''Retrieve 'mailbox' configuration for this task. Defaults to None.
        '''
        return self.CONF.get('mailbox')

    def search(self):
        '''
        Return mail message search criteria for this monitor task.

        Reference: c9r.mail.imap4
        '''
        return self.CONF.search

    def __call__(self, msg):
        '''
        Extract attachment(s) in a given email message that has already been parsed and
        save them to a folder as configured.
        '''
        raise Exception('Unhandled message (%s): (%s)'%(msg.get('uid', 'N/A'), msg.get('subject', 'N/A')))

    def __init__(self, conf, default_days=60):
        self.CONF = conf
        self.fetching = True
        self.days = datetime.timedelta(conf.get('days') or default_days)
