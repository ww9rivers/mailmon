#!/usr/bin/env python
#
## Module to move mail messages to a folder.

import datetime, os, re
from StringIO import StringIO
from FileMonitor import FileMonitor
from c9r.pylog import logger
from c9r.net import http


class Download(FileMonitor):
    '''
    Download file(s) linked in the message.
    '''
    def search(self):
        slist = list(self.CONF.get('search', []))
        slist.append((datetime.datetime.now()-self.days).strftime("SENTSINCE \"%d-%b-%Y\""))
        return slist

    def __call__(self, msg):
        ''' Parse the give msg['body'] for any URL to download file(s) from.

        Returns a list of files downloaded.
        '''
        end_dl = self.end_dl
        files = []
        linecnt = 0
        for line in StringIO(msg.get('body') or ''):
            mx = self.url.search(line)
            linecnt += 1
            if mx:
                url = mx.groups()[0]
                logger.debug('Downloading file: %s' % (url))
                fname = http.get(url, self.path, self.options)
                self.display(fname)
                files.append(fname)
            if end_dl:
                if isinstance(end_dl, int) and len(files) >= end_dl: break
                if end_dl.search(line): break
        logger.debug('Downloaded {0} files ({1} lines)'.format(len(files), linecnt))
        return files

    def __init__(self, conf):
        '''
        Configure this object: Get extra attributes for this object.

        /verify-cert/   True to verify server HTTPS certificate; Defaults to false.
        /end/           When to end download: A count, a regex, or False for everything in message.
        '''
        FileMonitor.__init__(self, conf)
        self.options = dict(verify = conf.get('verify-cert') or False)
	self.url = re.compile(conf.get('url') or "[\"'](http[^\"']+)")
        end_dl = conf.get('end') or False
        if isinstance(end_dl, basestring):
            end_dl = re.compile(end_dl)
        self.end_dl = end_dl


if __name__ == '__main__':
    import doctest
    doctest.testfile('test/Download.text')
