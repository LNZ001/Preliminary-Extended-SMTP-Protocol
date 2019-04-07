import esmtpd
import asyncore
import mailbox
import os
import time
import json


class CustomSMTPServer(esmtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print('Reciving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to:', rcpttos)
        print('Message length:', len(data))
        # print(data)

        # 存储邮件。
        mbox = mailbox.Maildir(rcpttos[0])
        # mbox.lock()
        # try:
        #     msg = mailbox.mboxMessage()
        #     msg.set_unixfrom('%s %s' % ( mailfrom, time.time()))
        #     msg['From'] = mailfrom
        #     msg['To'] = rcpttos
        #     msg['Subject'] =
        #     mbox.add(msg)
        print(os.path.join('./%s/new/%s.txt' % (rcpttos[0], str(time.time()))))
        with open(os.path.join('./%s/new/%s.txt' % (rcpttos[0], str(time.time()))), 'w', encoding="UTF-8") as file:
            file.write(data.decode())


server = CustomSMTPServer(('127.0.0.1', 1234), None)

asyncore.loop()

