#!/usr/bin/python
#
## $Id: mailmon.py,v 1.6 2015/06/11 21:40:49 weiwang Exp $
##
## Program to monitor mailbox and automatically handle messages.


import atexit, smtplib, sys
from c9r.app import Command
from c9r.mail import imap4, parser
from c9r.pylog import logger


class MailMonitorApp(Command):
    """
    """
    # Keep the MailMonitor.__doc__ empty to use the generic usage message in Command.
    def_conf = '/opt/miops/etc/mailmonitor-conf.json'

    def archive(self, auid, abox=''):
        """
        Archive a given message to the configured archive mail box. The mail box is created if it does not exist.
        """
        if not abox:
            abox = self.CONF.get('archive', '')
            if not abox:
                return None
        xcopy = self.mbox.archive(auid, abox)
        logger.debug("Archive: copy('%s') == %s" % (auid, xcopy))
        return xcopy

    def cleanup(self):
        '''Expunge (cleanup) the mailbox if configured so.
        '''
        if self.CONF.expunge:
            mbox = getattr(self, 'mbox', None)
            if hasattr(mbox, 'expunge'):
                for abox in self.cleanup_set:
                    mbox.select(abox)
                    mbox.expunge()

    def send(self, msg, msguid):
        """
        Resend a given message that has been edited as configured.
        """
        # Build TO:, CC: and BCC: lists into one list:
        addr = {'to':set(), 'cc':set(), 'bcc':set()}
        header = []
        for xk, xv in msg.items():
            xklo = xk.lower()
            if xklo in addr:
                logger.debug("mailmon.send: key = %s, value = %s" % (xk, xv))
                addr[xklo] |= set(re.split('[\s,:|]+', xv))
            elif xk != 'body': # -- excluding anything not belong in the header
                header.append(xk+': '+xv)

        # Get rid of any duplicates in the "to", "cc" and "bcc" list:
        if addr['to']:
            header.append('to: '+','.join(addr['to']))
            addr['cc'] -= addr['to']
            addr['bcc'] -= addr['to']
        if addr['cc']:
            header.append('cc: '+','.join(addr['cc']))
            addr['bcc'] -= addr['cc']
            addr['to'] |= addr['cc']
        if addr['bcc']:
            header.append('bcc: '+','.join(addr['bcc']))
            addr['to'] |= addr['bcc']

        nl = self.newline
        self.smtp.sendmail(msg['from'], addr['to'], nl.join(header)+nl+nl+msg['body'])

    def __call__(self):
        """
        Go throught the configured "task" list to run them.

        A task has these options:

        "archive"       Set to a folder to archive messages, or False to not archive;
                                Defaults to None -- to use global config.
        "fetch"         Set to False if no fetching is needed; Defaults to True.
        """
        xc = self.CONF
        logger.debug("mailmon: called, IMAP = %s:%d" % (xc.imap.server, xc.imap.port))
        try:
            self.mbox = imap4.Mailbox(xc)
        except Exception as xerr:
            print('Failed to connect IMAP server for checking email: %s' % (xerr))
            return -1

        # Search for message
        for xtask in self.task:
            taskbox = xtask.mailbox() or 'INBOX'
            self.mbox.select(taskbox)
            self.cleanup_set.add(taskbox)
            xres, xuid = self.mbox.search(xtask.search())
            logger.debug("IMAP.search => type = %s, data = %d:%s" % (xres, len(xuid), xuid))
            if not xuid[0]:
                continue
            for auid in xuid[0].split():
                if xtask.ignores_message(self.mbox, auid):
                    continue
                if xtask.fetching is not False:
                    result, data = self.mbox.fetch(auid)
                    if result != 'OK' or not isinstance(data, list):
                        logger.warn("Bad IMAP.fetch{0} result: {1}, {2}".format(auid, result, data))
                        continue
                abox = xtask.archive()
                if abox is not False: self.archive(auid, abox)
                if xtask.fetching is not False:
                    msg = self.parse(data[0][1])
                    if msg:
                        logger.debug("IMAP.fetched: uid = %s, msg.subject = %s" % (auid, msg['subject']))
                        xtask(msg)
            pass # end of all message for one task
        pass # end of tasks
        self.smtp.quit()
        sys.exit(0)

    def __init__(self):
        '''
        A command line application object to monitor email.

        The class must either have no doc, or have something in the format of c9r.app.Command.
        '''
        Command.__init__(self)
        xc = self.CONF
        smtp = self.CONF.smtp
        try:
            self.smtp = smtplib.SMTP(smtp.server, smtp.port)
        except Exception as xerr:
            raise Exception('Failed to connect SMTP server for sending email: %s' % (xerr))
        self.task = []
        plugin = xc.get('plugin', 'MailMonitor')
        mmmod = __import__(plugin+'.'+plugin)
        base_klass = getattr(getattr(mmmod, plugin, None), plugin, None)
        logger.debug("mailmon: Plugin base '%s' loaded as %s from %s."%(plugin, format(base_klass), format(mmmod)))
        for xtask in xc.get('tasklist', []):
            conf = xc.get(xtask)
            action = conf.action
            if not action:
                logger.error("mailmon: Task '%s' with no action is ignored."%(xtask))
                continue
            klass = getattr(globals(), action, None) # "action" class may be in globally defined
            if not klass and mmmod:
                mod = __import__(plugin+'.'+action)  # "action" class may also be in a plugin module
                if isinstance(mod, type(mmmod)):
                    klass = getattr(getattr(mod, action, None), action, None)
                    logger.debug("mailmon: Action '%s' imported as %s."%(action, str(klass)))
            if callable(klass) and issubclass(klass, base_klass):
                conf.util = self
                self.task.append(klass(conf))
            else:
                logger.error("mailmon: Action module '%s' is not callable."%(format(klass)))
                logger.error("mailmon: Action module '%s' not found, task '%s' is ignored."%(action, xtask))
        self.parse = parser.Parser()
        self.cleanup_set = set()
        atexit.register(self.cleanup)


if __name__ == '__main__':
    app = MailMonitorApp()
    if not app.dryrun:
        app()
