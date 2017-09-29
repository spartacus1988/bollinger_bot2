import numpy as np
from sortedcontainers import SortedDict
import matplotlib.pyplot as plt

class bb_math:

    def __init__(self):
        self.input_dict = SortedDict(
            {1506704760: 4218, 1506704820: 4218, 1506704880: 4220, 1506704940: 4218, 1506705000: 4220,
             1506705060: 4220, 1506705120: 4220, 1506705180: 4225, 1506705240: 4230, 1506705300: 4229,
             1506705360: 4220, 1506705420: 4225, 1506705480: 4225, 1506705540: 4225, 1506705600: 4225,
             1506705660: 4229, 1506705720: 4229, 1506705780: 4230, 1506705840: 4232, 1506705900: 4229,
             1506705960: 4218})

        # self.input_dict = SortedDict(
        #     {1506705360: 4220, 1506705420: 4225, 1506705480: 4225, 1506705540: 4225, 1506705600: 4225,
        #      1506705660: 4229, 1506705720: 4229, 1506705780: 4230, 1506705840: 4232, 1506705900: 4229,
        #      1506705960: 4218, 1506706020: 4229, 1506706080: 4229, 1506706140: 4229, 1506706200: 4207,
        #      1506706260: 4190, 1506706320: 4190, 1506706380: 4186, 1506706440: 4177, 1506706500: 4160,
        #      1506706560: 4165})



        self.running_avg = {}
        self.std_value = None
        #self.upper_line = None
        self.upper_line = {}
        #self.lower_line = None
        self.lower_line = {}



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
        upper_line = float(self.running_avg.values()[-1:][0]) + (2 * self.std_value)
        #print(self.upper_line)

        time_st = self.running_avg.keys()[-1:][0]
        self.upper_line[time_st] = upper_line
        # print(self.prices)
        # print(type(self.prices))
        self.upper_line = SortedDict(self.upper_line)
        return self.upper_line


    def bb_lower_line(self):
        #print(float(self.running_avg.values()[-1:][0]))
        lower_line = float(self.running_avg.values()[-1:][0]) - (2 * self.std_value)
        #print(self.lower_line)

        time_st = self.running_avg.keys()[-1:][0]
        self.lower_line[time_st] = lower_line
        self.lower_line = SortedDict(self.lower_line)
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
        #plt.show()
        plt.savefig("fig_1")



def main():
    pass

    running_avg_FIRST = []
    running_avg_SECOND = []
    running_avg_THIRD = []

    math = bb_math()
    print(math.input_dict)
    print(len(math.input_dict))
    math.running_avg = math.moving_average_FOUR(math.input_dict)

    #print("math.running_avg FIRST")
    #running_avg_FIRST = math.running_avg
    #print(set(math.running_avg.keys()))


    #running_avg_SECOND = math.moving_average_dict(math.running_avg)
    #print("math.running_avg SECOND")
    #print(running_avg_SECOND)

    #running_avg_THIRD = math.moving_average_dict(running_avg_SECOND)
    #running_avg_THIRD = math.moving_average_dict(running_avg_THIRD)
    #print("math.running_avg THIRD")
    #print(running_avg_THIRD)
    #running_avg_FIRST = math.moving_average_FOUR(math.input_dict)

    #math.bb_plot(math.input_dict, math.running_avg, running_avg_FIRST, running_avg_FIRST )







    math.std_dict = math.bb_std(math.input_dict)
    math.upper_line = math.bb_upper_line()
    math.lower_line = math.bb_lower_line()


    print(math.input_dict.values()[-1:][0])
    print(math.std_value)
    print(math.running_avg.values()[-1:][0])
    print(math.upper_line)
    print(math.lower_line)


    # if (math.input_dict.values()[-1:][0] < (math.lower_line + ((math.upper_line - math.lower_line) * 0.05))):
    #     print("HALF")
    # else:
    #     print("FLAH")
    # print(math.input_dict.values()[-1:][0])
    # print(math.upper_line - ((math.upper_line - math.lower_line) * 0.05))
    # print(math.upper_line)
    # print(math.lower_line + ((math.upper_line - math.lower_line) * 0.05))
    # print(math.lower_line)


    # if (math.input_dict.values()[-1:][0] < (math.lower_line + ((math.upper_line - math.lower_line) * 0.05))) and (math.input_dict.values()[-1:][0] > math.lower_line):
    #     print("COMPLETE")

    if (math.bb_compare_to_buy(math.input_dict.values()[-1:][0],math.lower_line.values()[-1:][0], math.upper_line.values()[-1:][0] )):
        print("BUY")

    if (math.bb_compare_to_sell(math.input_dict.values()[-1:][0], math.lower_line.values()[-1:][0], math.upper_line.values()[-1:][0])):
        print("SELL")


    math.bb_plot(math.input_dict, math.running_avg, math.upper_line, math.lower_line)

    #print(math.running_avg)
    #print(len(math.running_avg))







if __name__ == "__main__":
    main()