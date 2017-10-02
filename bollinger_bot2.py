import time
import bb_api
import bb_math
import bb_mail


def main():
    first_one = True
    while True:
        time_before = time.time()

        #get all instance objects
        if first_one: api = bb_api.bb_api(); math = bb_math.bb_math(); mail = bb_mail.bb_mail()

        #get all needed cryptocurrency
        api.merged_currencies = api.check_all_coins('all_coins.txt')

        #get SortedDict({time:price}) from time_before
        api.build_url_crypto_compare('BTC', 'USD', str(int(time_before)))
        api.json_crypto_compare = api.request(api.url_crypto_compare)
        temp_result = api.extract_crypto_compare()

        #get input_dict for math
        math.input_dict = temp_result

        #calculating mov_avg
        math.running_avg = math.moving_average_FOUR(math.input_dict)

        #calculating std
        math.std_dict = math.bb_std(math.input_dict)

        #calculating upper_line
        #print(math.running_avg)
        math.upper_line = math.bb_upper_line()

        #calculating lower_line
        math.lower_line = math.bb_lower_line()


        print("debug")
        math.bb_plot(math.input_dict, math.running_avg, math.upper_line, math.lower_line)
        mail.mail_send('Usernames.txt', str(math.bb_compare_to_sell(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0],math.upper_line.values()[-1:][0])), math.input_dict.values()[-1:][0], str(math.bb_compare_to_buy(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0],math.upper_line.values()[-1:][0])), 'fig_1.png')
        #print("after_debug")



        #SIGNAL to BUY
        if (math.bb_compare_to_buy(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0],math.upper_line.values()[-1:][0])):
            #print("BUY")
            math.bb_plot(math.input_dict, math.running_avg, math.upper_line, math.lower_line)
            mail.mail_send('Usernames.txt', 'BTC', math.input_dict.values()[-1:][0], 'buying', 'fig_1.png')

        #SIGNAL to SELL
        if (math.bb_compare_to_sell(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0],math.upper_line.values()[-1:][0])):
            #print("SELL")
            math.bb_plot(math.input_dict, math.running_avg, math.upper_line, math.lower_line)
            mail.mail_send('Usernames.txt', 'BTC', math.input_dict.values()[-1:][0], 'selling', 'fig_1.png')

        #delay for 5 minutes
        time_after = time.time()
        delta_time = time_after - time_before
        print("delta_time is "+ str(delta_time))
        first_one = False
        time.sleep(30 - delta_time)

if __name__ == "__main__":
     #
     # while True:
     #     try:
              main()
     #     except:
     #         pass
     #         print('error')
     #         continue
