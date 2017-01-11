#!/usr/bin/env python
#
## Module to move mail messages to a folder.

from Delete import Delete
from c9r.pylog import logger


class Move(Delete):
    '''
    Move/archive old email messages.
    '''
    def ignores_message(self, mbox, auid):
        '''Returns true if the message is deleted.
        '''
        if self.limit > 0:
            logger.info("MailMonitor.{0}: uid = {1}".format(type(self).__name__, auid))
            self.limit -= 1
        return False

    def __init__(self, conf, default_days=0):
        '''
        Configure this object: Force "archive".
        '''
        Delete.__init__(self, conf, default_days)
        if not self.archive(): self.CONF['archive'] = 'Archive'


if __name__ == "__main__":
    import doctest
    doctest.testfile('test/Move.text')
