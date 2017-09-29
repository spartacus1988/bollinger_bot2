import os
import datetime
import mimetypes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class bb_mail:

    def __init__(self):
        self.addressee = []
        self.credentials = {}
        self.msg_sub = None
        self.msg_body = None

    def extract_mail_data(self, pathfile):
        self.addressee = []
        self.credentials = {}
        with open(pathfile, 'r') as f:
            for line in f:
                user, pwd = line.strip().split(':')
                self.credentials[user] = pwd
                break
            for line in f:
                user, pwd = line.strip().split(':')
                self.addressee.append(user)
                break

    def create_msg_sub(self, sym, price):
        if (sym == 'BTC'):
            self.msg_sub = "Price Alert (BTRX " + sym + "/USD @ " + str(price) + ")"
        else:
            self.msg_sub = "Price Alert (BTRX " + sym + "/BTC @ " + str(price) + ")"
        return self.msg_sub

    def create_msg_body(self, sym, rate):
        if (sym == 'BTC'):
            self.msg_body = "Price for " + sym + " currency is within a " + rate + " range.\n" \
                            "https://www.coinigy.com/main/markets/BTRX/" + sym + "/USD.\n" \
                            "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n"
        else:
            self.msg_body = "Price for " + sym + " currency is within a " + rate + " range.\n" \
                            "https://www.coinigy.com/main/markets/BTRX/" + sym + "/BTC.\n" \
                            "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n"
        return self.msg_body


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

    def mail_send(self, path_to_file_credentials, currency, last_price, rate, path_to_fig ):
        self.extract_mail_data(path_to_file_credentials)
        self.msg_sub = self.create_msg_sub(currency, last_price)
        self.msg_body = self.create_msg_body(currency, rate)
        self.send_mail(self.msg_sub, self.msg_body, path_to_fig)



def main():
    pass
    mail = bb_mail()
    print(mail.credentials.keys())
    print(mail.addressee)
    mail.extract_mail_data("Usernames.txt")
    print(mail.credentials.keys())
    print(mail.addressee)

    #mail.send_mail("TEST", "HELLO", '/home/mixxxxx/PycharmProjects/bollinger_bot2/fig_1.png')







if __name__ == "__main__":
    main()