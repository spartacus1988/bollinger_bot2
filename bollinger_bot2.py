
import time
import datetime
import numpy as np
import pprint
import requests
import json as jsn
from pymongo import MongoClient
import matplotlib.pyplot as plt












def main():
    first_one = True
    # https: // api.coinmarketcap.com / v1 / ticker /?limit = 5
    while True:
        print ("This prints once a 5 minutes.")
        #time.sleep(300)

        #getting request
        url = "https://api.coinmarketcap.com/v1/ticker/?limit=1"
        json = get_json(url)
        #print(json)
        parced_json = jsn.loads(json)
        #print(parced_json[1])


        #db init
        client = MongoClient('localhost', 27017)
        db = client.crypto_database
        cryptocurrences = db.cryptocurrences


        #db insert data
        cryptocurrences.insert_many(parced_json)
        #cryptocurrences.update(parced_json)

        #deleting duplicate of collection with same "last_updated"
        to_compare = []
        for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}).sort("last_updated", -1).limit(2):
            to_compare.append(cryptocurrency[u'last_updated'])
        #print(to_compare)
        #print(to_compare[0])
        #print(to_compare.__len__())
        #print(db.cryptocurrences.count())
        if to_compare.__len__() > 1  and to_compare[0] == to_compare[1]:
            result = db.cryptocurrences.remove({u'name': "Bitcoin", u'last_updated': to_compare[0]})
            #print(result)

        #show all database
        for cryptocurrency in cryptocurrences.find():
            pass
            #pprint.pprint(cryptocurrency)

        #show all Bitcoin prices in db
        #for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}):
            #pprint.pprint(cryptocurrency)
            #pprint.pprint(float(cryptocurrency[u'price_usd']))
            #running_avg.append(float(cryptocurrency[u'price_usd']))


        #calculating moving average for last updated price in result_to_update
        running_avg = []
        for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}).sort("last_updated", -1).limit(3):
            #pprint.pprint(cryptocurrency)
            #pprint.pprint(float(cryptocurrency[u'price_usd']))
            running_avg.append(float(cryptocurrency[u'price_usd']))
        result_to_update = moving_average(running_avg, 3)
        print(result_to_update)


        #creating 'mov_avg' for last_updated point
        for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}).sort("last_updated", -1).limit(1):
            result = cryptocurrency.update({u'mov_avg': float(result_to_update)})
            print(result)
            result = cryptocurrences.save(cryptocurrency)
            print(result)


        #deleting part of collection with condition
        #result = db.cryptocurrences.remove({u'name': "Bitcoin"})
        #print(result)


        # calculating numpy std for last updated price in result_to_update
        running_avg = []
        for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}).sort("last_updated", 1).limit(20):
            # pprint.pprint(cryptocurrency)
            # pprint.pprint(float(cryptocurrency[u'price_usd']))
            running_avg.append(float(cryptocurrency[u'price_usd']))
        result_to_update = np.std(running_avg)
        print(running_avg)
        print(result_to_update)


        # creating 'upper_bb_line' and 'lower_bb_line' for last_updated point
        for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}).sort("last_updated", -1).limit(1):
            #upper line
            print(float(cryptocurrency[u'mov_avg']))
            result = cryptocurrency.update({u'upp_bbl': float(cryptocurrency[u'mov_avg']) + 2 * float(result_to_update)})
            print(result)
            result = cryptocurrences.save(cryptocurrency)
            print(result)
            #lower line
            result = cryptocurrency.update({u'low_bbl': float(cryptocurrency[u'mov_avg']) - 2 * float(result_to_update)})
            print(result)
            result = cryptocurrences.save(cryptocurrency)
            print(result)



        # creating charts
        x = []
        y = []
        z = []
        u_bbl = []
        l_bbl = []

        for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}).sort("last_updated", -1).limit(30):
            x.insert(0, float(cryptocurrency[u'last_updated']))
            y.insert(0, float(cryptocurrency[u'price_usd']))
            z.insert(0, float(cryptocurrency[u'mov_avg']))
            u_bbl.insert(0, float(cryptocurrency[u'upp_bbl']))
            l_bbl.insert(0, float(cryptocurrency[u'low_bbl']))

        # plt.plot(x, y)
        if first_one:
            plt.grid()
            my_labels = {"y": "price_usd", "z": "mov_avg", "u_bbl": "upp_bbl", "l_bbl": "low_bbl"}
        else:
            my_labels = {"y": "_nolegend_", "z": "_nolegend_", "u_bbl": "_nolegend_", "l_bbl": "_nolegend_"}
        scat1 = plt.plot(x, y, color='red', marker='o', linestyle='--', label=my_labels["y"])
        scat2 = plt.plot(x, z, color='blue', marker='o', linestyle='--', label=my_labels["z"])
        scat3 = plt.plot(x, u_bbl, color='green', marker='o', linestyle='--', label=my_labels["u_bbl"])
        scat4 = plt.plot(x, l_bbl, color='green', marker='o', linestyle='--', label=my_labels["l_bbl"])
        # plt.grid()
        plt.legend(loc='best')
        plt.show()
        plt.savefig("fig_1")




        #sending to e-mail with condition
        for cryptocurrency in cryptocurrences.find({u'name': u'Bitcoin'}).sort("last_updated", -1).limit(3):

            print("условие")
            print(float(cryptocurrency[u'price_usd']))
            print(">")
            print(float(cryptocurrency[u'upp_bbl']) - ((float(cryptocurrency[u'upp_bbl'])-float(cryptocurrency[u'low_bbl'])) * 0.05))



            if ((float(cryptocurrency[u'price_usd']) < (float(cryptocurrency[u'low_bbl']) + ((float(cryptocurrency[u'upp_bbl'])-float(cryptocurrency[u'low_bbl'])) * 0.05))) and (float(cryptocurrency[u'price_usd']) > float(cryptocurrency[u'low_bbl']))):
                msg_sub =  "Price Alert (BTRX " + cryptocurrency[u'symbol'] + "/USD @ " + cryptocurrency[u'price_usd'] + ")"
                msg_body = "Price for " + cryptocurrency[u'name'] + " currency is within a buying range.\n" \
                           "https://www.coinigy.com/main/markets/BTRX/" + cryptocurrency[u'symbol'] + "/USD.\n" \
                           "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n"
                credentials, addressee = extract_mail_data()

                for username in credentials:
                    send_mail(username, credentials[username], addressee, msg_sub, msg_body)

            elif ((float(cryptocurrency[u'price_usd']) > (float(cryptocurrency[u'upp_bbl']) - ((float(cryptocurrency[u'upp_bbl'])-float(cryptocurrency[u'low_bbl'])) * 0.05))) and (float(cryptocurrency[u'price_usd']) < float(cryptocurrency[u'upp_bbl']))):

                msg_sub =   "Price Alert (BTRX " + cryptocurrency[u'symbol'] + "/USD @ " + cryptocurrency[u'price_usd'] + ")"
                msg_body =  "Price for " + cryptocurrency[u'name'] + " currency is within a selling range.\n" \
                            "https://www.coinigy.com/main/markets/BTRX/" + cryptocurrency[u'symbol'] + "/USD.\n" \
                            "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n"
                credentials, addressee = extract_mail_data()

                for username in credentials:
                    send_mail(username, credentials[username], addressee, msg_sub, msg_body)

            elif float(cryptocurrency[u'price_usd']) < float(cryptocurrency[u'low_bbl']):

                msg_sub =  "Price Alert (BTRX " + cryptocurrency[u'symbol'] + "/USD @ " + cryptocurrency[u'price_usd'] + ")"
                msg_body = "Price for " + cryptocurrency[u'name'] + " currency is within a selling range.\n" \
                           "https://www.coinigy.com/main/markets/BTRX/" + cryptocurrency[u'symbol'] + "/USD.\n" \
                           "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n"
                credentials, addressee = extract_mail_data()

                for username in credentials:
                    send_mail(username, credentials[username], addressee, msg_sub, msg_body)

            elif float(cryptocurrency[u'price_usd']) > float(cryptocurrency[u'upp_bbl']):

                msg_sub =  "Price Alert (BTRX " + cryptocurrency[u'symbol'] + "/USD @ " + cryptocurrency[u'price_usd'] + ")"
                msg_body = "Price for " + cryptocurrency[u'name'] + " currency is within a buying range.\n" \
                           "https://www.coinigy.com/main/markets/BTRX/" + cryptocurrency[u'symbol'] + "/USD.\n" \
                           "Timestamp: " + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "\n"
                credentials, addressee = extract_mail_data()

                for username in credentials:
                    send_mail(username, credentials[username], addressee, msg_sub, msg_body)

        # show all database
        for cryptocurrency in cryptocurrences.find():
            pass
            #pprint.pprint(cryptocurrency)




        # show all database
        for cryptocurrency in cryptocurrences.find():
            pass
            #pprint.pprint(cryptocurrency)


        #calculating size of db and cleen it, if it's needed
        #time.time()-1_000_000 is for 10 days ago
        #week_ago = time.time()-1000000 + 999999
        week_ago = time.time() - 1000000
        mod = {"$lt": {}}
        mod["$lt"] = str(week_ago)
        #print(week_ago)
        #print(mod)
        #for cryptocurrency in cryptocurrences.find({u'name': "Bitcoin", u'last_updated': {"$lt": "1506285336"}}):

        #for cryptocurrency in cryptocurrences.find({u'name': "Bitcoin", u'last_updated': mod}):
            #print("less then \n")
            #print(cryptocurrency)
            #print(time.time()-1000000)
        result = db.cryptocurrences.remove({u'name': "Bitcoin", u'last_updated': mod})
        #print(result)


        #delay for 5 minutes
        first_one = False
        time.sleep(300)


if __name__ == "__main__":
    main()