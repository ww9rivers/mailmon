#!/usr/bin/env python
#
## Module to move mail messages to a folder.

import datetime, os
from MailMonitor import MailMonitor


class Move(MailMonitor):
    '''
    Move/archive old email messages.
    '''
    def search(self):
        slist = list(self.CONF.get('search', []))
        slist.append((datetime.datetime.now()-self.days).strftime("SENTBEFORE \"%d-%b-%Y\""))
        return slist

    def __init__(self, conf, default_days=1):
        '''
        Configure this object.
        '''
        MailMonitor.__init__(self, conf)
        days = conf.get('days', default_days)
        self.days = datetime.timedelta(days)
        if conf.util.debug:
            conf.util.log_debug("MailMonitor.Move: days = %d" % (days))
