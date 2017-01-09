#!/usr/bin/env python
#
## $Id: Delete.py,v 1.6 2015/04/17 21:26:48 weiwang Exp $
##
## Module to extract and save attachments in mail messages.

import datetime, os
from MailMonitor import MailMonitor
from c9r.pylog import logger


class Delete(MailMonitor):
    '''
    Delete old email messages.
    '''
    def ignores_message(self, mbox, auid):
        '''Returns true if the message is deleted.
        '''
        if self.limit > 0:
            logger.info("MailMonitor.Delete: uid = %s" % (auid))
            self.limit -= 1
            mbox.delete(auid)
        return self.stop

    def search(self):
        '''Build message searcg criteria for messages send before configured
        number of days.

        Returns a list of search criteria for this task.
        '''
        slist = list(self.CONF.get('search', []))
        slist.append((datetime.datetime.now()-self.days).strftime("SENTBEFORE \"%d-%b-%Y\""))
        return slist

    def __call__(self, msg):
        '''A message that reached this point is ignored due to configured 'limit'.
        '''
        logger.debug('Ignored message (%s): (%s)'%(msg.get('uid', 'N/A'), msg.get('subject', 'N/A')))

    def __init__(self, conf):
        '''Configure this object.

        .days   Only delete mails older than given number of days. Defaults to 60.
        .limit  Only delete up to given number of messages. Defaults to 1000.
        .stop   True if not continuing to process the messages found by this task.
        '''
        MailMonitor.__init__(self, conf)
        days = conf.get('days', 60)
        self.days = datetime.timedelta(days)
        self.limit = conf.get('limit', 1000)
        self.stop = conf.get('stop', True)
        self.fetching = conf.get('fetch') or False
        if conf.util.debug:
            logger.debug("MailMonitor.Delete: days = {0}, limit = {1}".format(days, self.limit))

if __name__ == "__main__":
    import doctest
    doctest.testfile('test/Delete.text')
