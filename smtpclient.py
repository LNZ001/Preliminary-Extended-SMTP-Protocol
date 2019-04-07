import smtplib
import email.utils
from email.mime.text import MIMEText
import mailbox
import esmtpd
import json
import getpass
from warnings import warn
import os


class ESMTP(smtplib.SMTP):
    def register(self):
        self.putcmd('REGI')
        return self.getreply()[0]

    def username(self, username):
        self.putcmd('USER', username)
        return self.getreply()[0]

    def passwd(self, passwd):
        self.putcmd('PSWD', passwd)
        return self.getreply()[0]

    def login(self, user, password, *, initial_response_ok=True):
        """Log in on an SMTP server that requires authentication.

        The arguments are:
            - user:         The user name to authenticate with.
            - password:     The password for the authentication.

        This method will return normally if the authentication was successful.
        """

        self.ehlo_or_helo_if_needed()
        # if not self.has_extn("auth"):
        #     raise SMTPNotSupportedError(
        #         "SMTP AUTH extension not supported by server.")

        self.putcmd('LOGINUSER', user)
        self.getreply()
        self.putcmd('LOGINPASSWD', password)
        return self.getreply()[0]


# 登录email客户端
print('Welcome to the lnz\'s email server.')

server = ESMTP('127.0.0.1', 1234)
# server.set_debuglevel(True)

# 选择注册/登录
while(True):

    op = input('选择注册/登录/退出(R/L/Q):').upper()
    while (op != 'R') and (op != 'L') and (op != 'Q'):
        op = input('非法输入.请输入R/L/Q:').upper()
        continue

    server.ehlo('smtp.lnz.com')

    if op == 'R':
        # 请求注册
        if server.register() != 250:
            warn('当前不允许注册.')
            continue

        # 注册：无论成功失败返回主选择
        username = input('用户名:')
        while server.username(username) != 250:
            username = input('用户已存在，请重新输入用户名：')

        # passwd = input('输入密码：')
        passwd = getpass.getpass('输入密码:')
        if server.passwd(passwd) != 250:
            print('注册失败。')
            continue

        print('用户%s注册成功' % username) # 创建邮箱在服务器端实现。

    elif op == 'L':
        # 登录： 输入账号密码(mail from 时检查是否登录和from地址是否一致。)
        username = input('用户名:')
        # passwd = input('输入密码：')
        passwd = getpass.getpass('输入密码:')
        while server.login(username, passwd) != 250:
            print('密码错误或账户不存在，请重新输入。')
            username = input('用户名:')
            # passwd = input('输入密码：')
            passwd = getpass.getpass('输入密码:')

        print('用户%s登录成功' % username)

        ops = input('发送/接收邮件/退出：(R/S/Q)').upper()
        while (ops != 'R') and (ops != 'S') and (ops != 'Q'):
            ops = input('发送/接收邮件/退出：(R/S/Q)').upper()

        if ops == 'S':

            # Create the message
            # 默认只能使用自己的账号发，服务器端进行检查。
            msgContent = input('邮件内容：')
            msg = MIMEText(msgContent)

            msg['From'] = email.utils.formataddr((username.split('@')[0].upper(), username))

            msgTo = input('对方邮箱地址:')
            msg['To'] = email.utils.formataddr((msgTo.split('@')[0].upper(), msgTo))

            msg['Subject'] = input('邮件主题:')

            server.sendmail(username, [msgTo], msg.as_string())

            continue

        elif ops == 'R':
            for dirname, subdirs, files in os.walk(username):
                # print(dirname)
                # print('\tDirectories:', subdirs)
                for name in files:
                    fullname = os.path.join(dirname, name)
                    print()
                    print('***打开邮件：', fullname)
                    print(open(fullname).read())
                    print('*' * 20)
            continue
        else:
            server.quit()
            break
    else:
        server.quit()
        break


