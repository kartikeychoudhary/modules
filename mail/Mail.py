import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


user = "fsociety6778@gmail.com"
pas = "fsocietyrox!!"


class Mail:
    def __init__(self):
        self.init = 0

    def readmail(self):
        msr = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        msr.login(user, pas)
        stat, cnt = msr.select('inbox')
        stat, dta = msr.fetch(cnt[0], '(RFC822)')

        mail = email.message_from_bytes(dta[0][1])
        frad = str(mail['From'])
        frad = frad.split()
        fr = ''
        frus = str(frad[-1])
        for i in range(len(frus) - 1):
            if i > 0:
                fr = fr + frus[i]

        msr.store(cnt[0], '+FLAGS', '\\Deleted')

        for part in mail.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                msg = body.decode('utf-8')

        if "https://" not in msg:
            msg = msg + ' ' + fr
            msg = msg.split()
            return msg
        else:
            temp = []
            video_id = ""
            length = len(msg)
            for i in range(-1, -length, -1):
                if msg[i] == '=' or msg[i] == '/':
                    break
                video_id+=msg[i]
            if len(video_id) > 15:
                return None
            video_id = video_id[::-1]
            temp.append("youtube")
            temp.append(video_id)
            temp.append(fr)
            return temp

    def sendmail(self, fr, message, subject):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(user, pas)
        toaddrs = fr
        global userto
        userto = toaddrs
        msg = "\r\n".join([
            "From:" + user,
            "To:" + toaddrs,
            "Subject:" + subject,
            "",
            message
        ])
        server.sendmail(user, toaddrs, msg)

        server.quit()

    def sendmailHTML(self, fr, mtext, mhtml, subject):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(user, pas)
        toaddrs = fr
        global userto
        userto = toaddrs

        the_msg = MIMEMultipart("alternative")
        the_msg['Subject'] = subject
        the_msg["From"] = user
        the_msg["To"] = toaddrs

        plain_txt = mtext
        html_txt = mhtml

        part_1 = MIMEText(plain_txt, 'plain')
        part_2 = MIMEText(html_txt, 'html')

        the_msg.attach(part_1)
        the_msg.attach(part_2)
        
        server.sendmail(user, toaddrs, the_msg.as_string())

        server.quit()
