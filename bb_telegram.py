
from telegram.ext import Updater, CommandHandler, Job
import logging, yaml, sys, os




def init_log():
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        filename='bot.log',
        filemode='w',
    )

    logger = logging.getLogger(__name__)
    return logger


def get_config(path_to_config):
    # Trying to read config
    try:
        with open(path_to_config, 'r') as ymlfile:
            config = yaml.load(ymlfile)
    except BaseException:
        print(path_to_config + " file is not exists! Please create it first.")
        sys.exit()

    if config['token'] == '':
        print("Please configure your Telegram bot token")
        sys.exit()

    if len(config['files']) == 0:
        print("Please add some files to the config")
        sys.exit()

    if config['interval'] == 0 or config['interval'] == '':
        logger.warn('Notify interval is not set. I will send log files every 4 hours')
    config['interval'] = 4*60*60
    return config



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    bot.send_message(chat_id=-1001116291223, text="I'm a bot, please talk to me!")




def main():
    logger = init_log()
    config = get_config('config.yml')

    updater = Updater(config['token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    #dp.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
    #dp.add_handler(CommandHandler("help", start))
    #dp.add_handler(CommandHandler("cat", cat, pass_args=True))
    # dp.add_handler(CommandHandler("set", set, pass_args=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.




    # bot.sendMessage(
    #     -1001116291223,
    #     parse_mode="Markdown",
    #     text=(
    #         "Howdy!\n"
    #         "Write */cat* to output all configured files,\n"
    #         "or */cat *_filename_ _filename2_ ' ' to send only _filename_ and _filename2_ (those files must be defined in the config file)"
    #     )
    # )


    print('idle')
    updater.idle()












if __name__ == "__main__":
    main()