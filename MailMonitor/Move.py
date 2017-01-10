#!/usr/bin/env python
#
## Module to move mail messages to a folder.

from Delete import Delete


class Move(Delete):
    '''
    Move/archive old email messages.
    '''
    def __init__(self, conf, default_days=0):
        '''
        Configure this object: Force "archive".
        '''
        Delete.__init__(self, conf, default_days)
        self.stop = False
        if not self.archive(): self.CONF['archive'] = 'Archive'


if __name__ == "__main__":
    import doctest
    doctest.testfile('test/Move.text')
