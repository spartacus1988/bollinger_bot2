
from telegram.ext import Updater, CommandHandler, Job
import logging
import yaml
import sys
import os
import time



class bb_telegram():

    def __init__(self, token, chat_id):
        self.chat_id = chat_id
        self.token = token
        self.updater = Updater(self.token)
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start))
        self.updater.start_polling()
        #self.updater.idle()


    def start(self):
        #bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        #bot.send_message(chat_id=1116291223, text="I'm a bot, please talk to me!")
        #bot.send_message(chat_id=683976468, text="I'm a bot, please talk to me!")
        self.dp.bot.send_message(chat_id=self.chat_id, text="I'm starting now!")
        print("message was send")


    def send(self):
        self.dp.bot.send_message(chat_id=self.chat_id, text="I'm a bot, please talk to me!")
        print("message was send")



def main():

    try:
        with open('config.yml', 'r') as ymlfile:
            config = yaml.load(ymlfile)
    except BaseException:
        print(path_to_config + " file is not exists! Please create it first.")
        sys.exit()

    token = config['token']
    chat_id = config['users'][0]
    telegram = bb_telegram(token, chat_id)
    telegram.send()


if __name__ == "__main__":
    main()