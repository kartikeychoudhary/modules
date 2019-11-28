import os
from util import loadCredentials
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail:
    def __init__(self):
        self.init = 0
        credentials = loadCredentials()
        self.username = credentials[0]
        self.password = credentials[1]
        try:
            self.msr = imaplib.IMAP4_SSL('imap.gmail.com', 993)
            self.msr.login(self.username, self.password)
        except:
            print("Error while IMAP")
        try:
            self.smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.smtp.login(self.username, self.password)
        except:
            print("Error while SMTP")

    def deleteMail(self, index):
        stat, cnt = self.msr.select('inbox')
        self.msr.store(cnt[index], '+FLAGS', '\\Deleted') # first select the inbox

    def readFirstMail(self):
        stat, cnt = self.msr.select('inbox')
        index_mail = 0
        stat, data = self.msr.fetch(cnt[index_mail], '(RFC822)')
        mail = email.message_from_bytes(data[0][1])

        from_address = str(mail['From'])
        name = from_address[:from_address.index('<')]
        from_address = from_address[from_address.index('<')+1:from_address.index('>')]
          
        for part in mail.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                msg = body.decode('utf-8')
        
        return [name, from_address, msg]
        

        
    def readMail(self):
        stat, cnt = self.msr.select('inbox')
        index_mail = 0
        stat, dta = self.msr.fetch(cnt[index_mail], '(RFC822)')
        mail = email.message_from_bytes(dta[0][1])
        frad = str(mail['From'])
        frad = frad.split()
        fr = ''
        frus = str(frad[-1])
        for i in range(len(frus) - 1):
            if i > 0:
                fr = fr + frus[i]

        self.msr.store(cnt[0], '+FLAGS', '\\Deleted')

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
                video_id += msg[i]
            if len(video_id) > 15:
                return None
            video_id = video_id[::-1]
            temp.append("youtube")
            temp.append(video_id)
            temp.append(fr)
            return temp

    def sendMail(self, sender, receiver, message, subject):
        msg = "\r\n".join([
            "From:" + sender,
            "To:" + receiver,
            "Subject:" + subject,
            "",
            message
        ])
        self.smtp.sendmail(sender, receiver, msg)
        self.smtp.quit()

    def sendmailHTML(self, sender,receiver, text, html, subject):
        the_msg = MIMEMultipart("alternative")
        the_msg['Subject'] = subject
        the_msg["From"] = sender
        the_msg["To"] = receiver

        plain_txt = text
        html_txt = html

        part_1 = MIMEText(plain_txt, 'plain')
        part_2 = MIMEText(html_txt, 'html')

        the_msg.attach(part_1)
        the_msg.attach(part_2)
        
        self.smtp.sendmail(sender, receiver, the_msg.as_string())
        self.smtp.quit()

    def youtubeTag(self, link):
        return link.split('/')[-1]
        