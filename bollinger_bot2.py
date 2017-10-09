import sys
import os
import datetime
import time
import bb_api
import bb_math
import bb_mail
import bb_telegram
import logging
import yaml



def init_log():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        filename='bot.log',
        filemode='w',
    )
    logger = logging.getLogger(__name__)
    return logger


def get_config(path_to_config):
    try:
        with open(path_to_config, 'r') as ymlfile:
            config = yaml.load(ymlfile)
    except BaseException:
        print(path_to_config + " file is not exists! Please create it first.")
        sys.exit()

    if config['token'] == '':
        print("Please configure your Telegram bot token")
        sys.exit()

    #if len(config['files']) == 0:
    #    print("Please add some files to the config")
    #    sys.exit()

    if config['interval'] == 0 or config['interval'] == '':
        logger.warn('Notify interval is not set. I will send log files every 4 hours')
        config['interval'] = 4*60*60
    return config



def send_handler(api, math, mail, config, cryptocurrency, rate):

    math.bb_plot(math.input_dict, math.running_avg, math.upper_line, math.lower_line, cryptocurrency)

    api.build_url_addinfo(cryptocurrency)
    api.json_addinfo = api.request(api.url_addinfo)
    vol_24h = api.extract_addinfo()

    if (config['e-mailing_status']):
        mail.mail_send(config['msg_from'], config['msg_to'], cryptocurrency, math.input_dict.values()[-1:][0], rate, vol_24h)


    if (config['telegram_status']):
        token = config['token']

        if (config['mode'] == 'PROD'):
            chat_id = config['users'][2]
        else:
            chat_id = config['users'][2]

        telegram = bb_telegram.bb_telegram(token, chat_id)

        telegram.send_message(cryptocurrency, rate, vol_24h)
        telegram.send_picture(cryptocurrency)

    if cryptocurrency is not 'BTC':
        try:
            os.remove(cryptocurrency + '_BTC.png')
        except:
            pass
    else:
        try:
            os.remove('BTC_USD.png')
        except:
            pass


def main():
    first_one = True

    while True:

        time_before = time.time()

        #get all instance objects
        if first_one: api = bb_api.bb_api(); math = bb_math.bb_math(); mail = bb_mail.bb_mail()

        #get all needed cryptocurrency
        api.merged_currencies = api.check_all_coins('all_coins.txt', config['min_Cap'], config['24hr_Vol'])



        for cryptocurrency in api.merged_currencies:
            #print(cryptocurrency)
            if cryptocurrency is not 'BTC':
                # get SortedDict({time:price}) from time_before
                api.build_url_crypto_compare(cryptocurrency, 'BTC', str(int(time_before)), config['limit'])
                #print(api.url_crypto_compare)
            else:
                api.build_url_crypto_compare('BTC', 'USD', str(int(time_before)), config['limit'])
                #print(api.url_crypto_compare)



            api.json_crypto_compare = api.request(api.url_crypto_compare)
            temp_result = api.extract_crypto_compare()

            #print(temp_result)

            if len(temp_result.keys()) != 0:

                #get input_dict for math
                math.input_dict = temp_result

                #calculating mov_avg
                math.running_avg = math.moving_average_FOUR(math.input_dict, config['num_avg'])

                #calculating std
                math.std_value = math.bb_std(math.input_dict)
                print('math.std_value is ')
                print(math.std_value)
                sys.stdout.flush()

                #calculating upper_line
                #print(math.running_avg)
                math.upper_line = math.bb_upper_line()

                #calculating lower_line
                math.lower_line = math.bb_lower_line()


                #print("debug")
                #send_handler(api, math, mail, config, cryptocurrency, 'debug')

                #SIGNAL to BUY
                if (math.bb_compare_to_buy(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0],math.upper_line.values()[-1:][0], config['percent'])) and (math.std_value > 0):
                    print("BUY " + cryptocurrency)
                    send_handler(api, math, mail, config, cryptocurrency, 'buying')

                #SIGNAL to SELL
                if (math.bb_compare_to_sell(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0],math.upper_line.values()[-1:][0], config['percent'])) and (math.std_value > 0):
                    print("SELL " + cryptocurrency)
                    send_handler(api, math, mail, config, cryptocurrency, 'selling')


        #delay for 5 minutes
        time_after = time.time()
        delta_time = time_after - time_before
        print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
        print("delta_time is " + str(delta_time))
        sys.stdout.flush()
        first_one = False
        time.sleep(config['interval'] - delta_time)


if __name__ == "__main__":

    logger = init_log()
    config = get_config('config.yml')

    if len(sys.argv) > 1:
        #print(format(sys.argv[1]))
        config['mode'] = format(sys.argv[1])
    else:
        print("No args")


    while True:
        try:
            main()
        except Exception as error:
            print(error)
            print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
            logger.error(error)
            sys.stdout.flush()
            continue
