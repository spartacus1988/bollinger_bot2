import numpy as np
from sortedcontainers import SortedDict
import matplotlib.pyplot as plt

class bb_math:

    def __init__(self):
        #self.input_dict = SortedDict({1506379680: 3934, 1506379920: 3925, 1506380460: 3933.9, 1506379620: 3949.4, 1506380280: 3933.9, 1506380520: 3927.54, 1506379560: 3950, 1506379500: 3950, 1506380100: 3925.1, 1506379980: 3925, 1506380400: 3933.9, 1506380340: 3930, 1506379440: 3950, 1506380040: 3925.1, 1506380160: 3933.99, 1506379860: 3925, 1506380580: 3927.54, 1506379800: 3935, 1506379380: 3945, 1506380220: 3934, 1506379740: 3935})
        # self.input_dict = SortedDict(
        #     {1506379680: 3934, 1506379920: 3925, 1506380460: 3933.9, 1506379620: 3949.4, 1506380280: 3933.9,
        #      1506380520: 3927.54, 1506379560: 3950, 1506379500: 3950, 1506380100: 3925.1, 1506379980: 3925,
        #      1506380400: 3933.9, 1506380340: 3930, 1506379440: 3950, 1506380040: 3925.1, 1506380160: 3933.99,
        #      1506379860: 3925, 1506380580: 3927.54, 1506379800: 3935, 1506379380: 3945, 1506380220: 3934,
        #      1506379740: 3935})

        self.input_dict = SortedDict(
            {1506677760: 4090, 1506677820: 4100, 1506677880: 4100, 1506677940: 4105,
             1506678000: 4100, 1506678060: 4102, 1506678120: 4100, 1506678180: 4100,
             1506678240: 4105, 1506678300: 4106, 1506678360: 4110, 1506678420: 4110,
             1506678480: 4110, 1506678540: 4115, 1506678600: 4114, 1506678660: 4119,
             1506678720: 4118.42, 1506678780: 4115, 1506678840: 4118.41,
             1506678900: 4116, 1506678960: 4119})
        self.running_avg = {}
        self.std_value = None
        self.upper_line = None
        self.lower_line = None



    def moving_average(self, x, N):
        if (len(x)<N):
            #print("x<N")
            return x[0]
        else:
            #print("x>N")
            #print(np.convolve(x, np.ones((N,)) / N)[(N-1):])
            #return np.convolve(x, np.ones((N,)) / N)[1:]
            #print(np.convolve(x, np.ones((N,)) / N, mode='valid')[-1:])
            return np.convolve(x, np.ones((N,)) / N, mode='valid')[-1:][0]


    def moving_average_dict(self, sorted_dict):
        tmp_lst = []
        #tmp_lst_mov = []
        #tmp_var = None
        for item in sorted_dict.keys():
            time_st = item
            price = sorted_dict[item]
            tmp_lst.append(price)
            tmp_var = self.moving_average(tmp_lst, 3)
            #tmp_lst_mov.append(tmp_var)
            self.running_avg[item] = tmp_var
        #print(tmp_lst_mov)
        #print(len(tmp_lst_mov))
        #print(self.running_avg)
        self.running_avg = SortedDict(self.running_avg)
        #print(self.running_avg)
        #print(len(self.running_avg))
        return self.running_avg

    def moving_average_FOUR(self, sorted_dict):
        for i in range(4):
            #print("ONE")
            sorted_dict = self.moving_average_dict(sorted_dict)
        return sorted_dict

    def bb_std(self, sorted_dict):
        self.std_value = np.std(sorted_dict.values())
        self.std_value = float(self.std_value)
        print(self.std_value)
        return self.std_value

    def bb_upper_line(self):
        #print(float(self.running_avg.values()[-1:][0]))
        self.upper_line = float(self.running_avg.values()[-1:][0]) + (2 * self.std_value)
        #print(self.upper_line)
        return self.upper_line

    def bb_lower_line(self):
        #print(float(self.running_avg.values()[-1:][0]))
        self.lower_line = float(self.running_avg.values()[-1:][0]) - (2 * self.std_value)
        #print(self.lower_line)
        return self.lower_line

    def bb_compare_to_buy(self, curPrice, lower_line, upper_line ):
        if ((curPrice < (lower_line + ((upper_line - lower_line) * 0.05))) and (curPrice > lower_line)) or curPrice > upper_line :
            return True
        else:
            return False

    def bb_compare_to_sell(self, curPrice, lower_line, upper_line):
        if ((curPrice > (upper_line - ((upper_line - lower_line) * 0.05))) and (curPrice < upper_line)) or curPrice < lower_line:
            return True
        else:
            return False

    def bb_plot(self, sort_Dict_price, sort_Dict_avg, sort_Dict_upp, sort_Dict_low):
        my_labels = {"sort_Dict_price": "price_usd", "sort_Dict_avg": "mov_avg", "sort_Dict_upp": "upp_bbl", "sort_Dict_low": "low_bbl"}
        scat1 = plt.plot(sort_Dict_price.keys(), sort_Dict_price.values(), color='red', marker='o', linestyle='--', label=my_labels["sort_Dict_price"])
        scat2 = plt.plot(sort_Dict_avg.keys(), sort_Dict_avg.values(), color='blue', marker='o', linestyle='--', label=my_labels["sort_Dict_avg"])
        scat3 = plt.plot(sort_Dict_upp.keys(), sort_Dict_upp.values(), color='green', marker='o', linestyle='--', label=my_labels["sort_Dict_upp"])
        scat4 = plt.plot(sort_Dict_low.keys(), sort_Dict_low.values(), color='yellow', marker='o', linestyle='--', label=my_labels["sort_Dict_low"])
        plt.grid()
        plt.legend(loc='best')
        plt.show()



def main():
    pass

    running_avg_FIRST = []
    running_avg_SECOND = []
    running_avg_THIRD = []

    math = bb_math()
    print(math.input_dict)
    print(len(math.input_dict))
    math.running_avg = math.moving_average_dict(math.input_dict)

    #print("math.running_avg FIRST")
    #running_avg_FIRST = math.running_avg
   # print(set(math.running_avg.keys()))


    running_avg_SECOND = math.moving_average_dict(math.running_avg)
    #print("math.running_avg SECOND")
    #print(running_avg_SECOND)

    #running_avg_THIRD = math.moving_average_dict(running_avg_SECOND)
    #running_avg_THIRD = math.moving_average_dict(running_avg_THIRD)
    #print("math.running_avg THIRD")
    #print(running_avg_THIRD)

    running_avg_FIRST = math.moving_average_FOUR(math.input_dict)

    math.bb_plot(math.input_dict, running_avg_SECOND, running_avg_FIRST, running_avg_FIRST )







    math.std_dict = math.bb_std(math.input_dict)
    math.upper_line = math.bb_upper_line()
    math.lower_line = math.bb_lower_line()


    print(math.input_dict.values()[-1:][0])
    print(math.std_value)
    print(math.running_avg.values()[-1:][0])
    print(math.upper_line)
    print(math.lower_line)


    if (math.input_dict.values()[-1:][0] < (math.lower_line + ((math.upper_line - math.lower_line) * 0.05))):
        print("HALF")
    else:
        print("FLAH")
    print(math.input_dict.values()[-1:][0])
    print(math.upper_line - ((math.upper_line - math.lower_line) * 0.05))
    print(math.upper_line)
    print(math.lower_line + ((math.upper_line - math.lower_line) * 0.05))
    print(math.lower_line)


    if (math.input_dict.values()[-1:][0] < (math.lower_line + ((math.upper_line - math.lower_line) * 0.05))) and (math.input_dict.values()[-1:][0] > math.lower_line):
        print("COMPLETE")

    if (math.bb_compare_to_buy(math.input_dict.values()[-1:][0],math.lower_line, math.upper_line )):
        print("BUY")

    if (math.bb_compare_to_sell(math.input_dict.values()[-1:][0], math.lower_line, math.upper_line)):
        print("SELL")


    #print(math.running_avg)
    #print(len(math.running_avg))







if __name__ == "__main__":
    main()