#!/usr/bin/env python
#
## Module to move mail messages to a folder.

from Delete import Delete


class Move(Delete):
    '''
    Move/archive old email messages.
    '''
    def __init__(self, conf, default_days=1):
        '''
        Configure this object.
        '''
        Delete.__init__(self, conf)
        if not slef.archive(): self.CONF['archive'] = 'Archive'
