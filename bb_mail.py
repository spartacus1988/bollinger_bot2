import os
import mimetypes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class bb_mail:

    addressee = []
    credentials = {}

    def extract_mail_data(self, pathfile):
        addressee = []
        credentials = {}
        with open(pathfile, 'r') as f:
            for line in f:
                user, pwd = line.strip().split(':')
                credentials[user] = pwd
                break
            for line in f:
                user, pwd = line.strip().split(':')
                addressee.append(user)
                break
        self.credentials, self.addressee = credentials, addressee

    def send_mail(self, msg_sub, msg_body, attach_path):
        msg = MIMEMultipart()
        msg['Subject'] = msg_sub
        msg['To'] = ','.join(self.addressee)
        text = MIMEText(msg_body)
        text.add_header("Content-Disposition", "inline")
        msg.attach(text)

        attach = MIMEApplication(open(attach_path, 'rb').read())
        filename = os.path.basename(attach_path)
        attach.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attach)

        for username in self.credentials:
            msg['From'] = username
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)       # connecting to gmail
            smtpObj.starttls()                                  # TLS(Transport Layer Security) on
            smtpObj.login(username, self.credentials[username])
            smtpObj.sendmail(username, self.addressee, msg.as_string())
            smtpObj.quit()




def main():
    pass
    mail = bb_mail()
    print(mail.credentials.keys())
    print(mail.addressee)
    mail.extract_mail_data("Usernames.txt")
    print(mail.credentials.keys())
    print(mail.addressee)

    mail.send_mail("TEST", "HELLO", '/home/mixxxxx/PycharmProjects/bollinger_bot2/fig_1.png')







if __name__ == "__main__":
    main()