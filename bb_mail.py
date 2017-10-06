import os
import datetime
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


    def send_mail(self, address,  msg_sub, msg_body, files):
        msg = MIMEMultipart()
        msg['Subject'] = msg_sub
        del msg['To']
        msg['To'] = address

        print(msg['To'])

        text = MIMEText(msg_body)
        text.add_header("Content-Disposition", "inline")
        msg.attach(text)

        for attach_path in files:
            attach = MIMEApplication(open(attach_path, 'rb').read())
            filename = os.path.basename(attach_path)
            attach.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attach)

        for username in self.credentials:
            msg['From'] = username
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)       # connecting to gmail
            smtpObj.starttls()                                  # TLS(Transport Layer Security) on
            smtpObj.login(username, self.credentials[username])
            smtpObj.sendmail(username, address, msg.as_string())
            smtpObj.quit()



    def mail_send(self, credentials, addressee,  currency, last_price, rate, files):
        for credential in credentials:
            user, pwd = credential.strip().split(':')
            self.credentials[user] = pwd
        self.addressee = addressee
        self.msg_sub = self.create_msg_sub(currency, last_price)
        self.msg_body = self.create_msg_body(currency, rate)

        for address in self.addressee:
             self.send_mail(address, self.msg_sub, self.msg_body, files)



def main():
    pass
    mail = bb_mail()


if __name__ == "__main__":
    main()