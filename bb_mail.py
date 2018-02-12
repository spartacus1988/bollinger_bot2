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

    def create_msg_body(self, sym, rate, vol_24h):
        if (sym == 'BTC'):
            self.msg_body = "Price for " + sym + " currency is within a " + rate + " range.\n" \
                            "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n" \
                            "24hr Vol: " + vol_24h + "\n"


        else:
            self.msg_body = "Price for " + sym + " currency is within a " + rate + " range.\n" \
                            "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n" \
                             "24hr Vol: " + vol_24h + "\n"

        return self.msg_body


    def send_mail(self, address,  msg_sub, msg_body, cryptocurrency):
        msg = MIMEMultipart()
        msg['Subject'] = msg_sub
        del msg['To']
        msg['To'] = address

        print(msg['To'])

        text = MIMEText(msg_body)
        text.add_header("Content-Disposition", "inline")
        msg.attach(text)


        if cryptocurrency is not 'BTC':
            filename = cryptocurrency + '_BTC.png'
        else:
            filename = 'BTC_USD.png'
        attach = MIMEApplication(open(filename, 'rb').read())
        attach.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attach)

        for username in self.credentials:
            msg['From'] = username
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)       # connecting to gmail
            smtpObj.starttls()                                  # TLS(Transport Layer Security) on
            smtpObj.login(username, self.credentials[username])
            smtpObj.sendmail(username, address, msg.as_string())
            smtpObj.quit()




    def mail_send(self, credentials, addressee,  cryptocurrency, last_price, rate, vol_24h):
        for credential in credentials:
            user, pwd = credential.strip().split(':')
            self.credentials[user] = pwd
        self.addressee = addressee
        self.msg_sub = self.create_msg_sub(cryptocurrency, last_price)
        self.msg_body = self.create_msg_body(cryptocurrency, rate, vol_24h)

        for address in self.addressee:
             self.send_mail(address, self.msg_sub, self.msg_body, cryptocurrency)



def main():
    pass
    mail = bb_mail()


if __name__ == "__main__":
    main()
